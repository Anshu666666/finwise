"""
================================================================================
FINWISE AI – OPENROUTER API CLIENT
Author: Zaid (Intelligent Agent & Web Search Lead)
================================================================================
Real OpenRouter LLM API client supporting configurable models (e.g. Gemini 2.0 Flash,
DeepSeek V3, Llama 3.3 70B, Claude 3.5 Sonnet) via OpenRouter's OpenAI-compatible API.
Zero fake responses. Zero silent fallbacks. Clear, structured error handling.
================================================================================
"""

import os
import time
import logging
from typing import Any, Dict, List, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("finwise.openrouter")

DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")
DEFAULT_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_TIMEOUT = float(os.getenv("OPENROUTER_TIMEOUT", "60.0"))

FREE_CANDIDATE_MODELS = [
    "openrouter/free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-small-24b-instruct-2501:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "google/gemma-2-9b-it:free",
]


import re

def clean_llm_response(raw_content: Optional[str]) -> str:
    """
    Extracts the user-facing response by stripping out internal chain-of-thought,
    reasoning tags, thinking blocks, and planning monologues.
    Ensures that ONLY the final response is shown to the user.
    """
    if not raw_content:
        return ""

    text = str(raw_content)

    # 1. Strip XML/HTML style reasoning tags
    patterns = [
        r"<think>.*?</think>",
        r"<thought>.*?</thought>",
        r"<reasoning>.*?</reasoning>",
        r"<reflection>.*?</reflection>",
        r"<internal_thought>.*?</internal_thought>",
        r"\[THINKING\].*?\[/THINKING\]",
        r"\[REASONING\].*?\[/REASONING\]",
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)

    # 2. Handle unclosed opening tags at the beginning (e.g. streaming/truncated <think> blocks)
    if "<think>" in text.lower():
        text = re.sub(r"^.*?<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"^.*?<think>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # 3. Strip labeled reasoning prefixes if formatted as plain text
    text = re.sub(r"^(?:Thought|Reasoning|Internal reasoning|Chain of thought|Analysis):\s*.*?\n\n", "", text, flags=re.DOTALL | re.IGNORECASE)

    # 4. Strip "Here's a thinking process:" or "Thinking Process:" or numbered planning blocks
    if re.search(r"^(?:Here'?s a thinking process|Thinking Process|Thought Process|Here is my thought process|\d+\.\s*\*\*(?:Analyze|Identify|Determine|Review|Understand|Formulate|Extract|Plan|Draft)|\*\*Step \d|\*\*\d+\.|\*\*Analysis:?\*\*):?", text.strip(), flags=re.IGNORECASE):
        # Check if there is an explicit transition separator
        parts = re.split(r"\n\s*(?:---|###\s*Response|\*\*Response:?\*\*|Final\s*(?:Response|Answer):?|\n(?=##\s|\*\*Why |\*\*Based on |\*\*The |\*\*Here |\*\*Your |\*\*Equity ))\s*\n", text, flags=re.IGNORECASE)
        if len(parts) > 1:
            text = parts[-1].strip()
        else:
            # Look for double newline before main content header
            split_header = re.search(r"\n\n(?=##\s|\*\*|Based on |Given |For your |To allocate |Your |Why |Prioritizing |Hello |Hi |Dear |Equity )", text, flags=re.IGNORECASE)
            if split_header:
                text = text[split_header.end():].strip()
            else:
                text = re.sub(r"^(?:Here'?s a thinking process|Thinking Process|Thought Process|Here is my thought process|\d+\.\s*\*\*[^\n]*\n):\s*", "", text, flags=re.IGNORECASE).strip()

    # 5. Strip leading internal monologue lines if the model leaks planning steps
    lines = text.split("\n")
    cleaned_lines = []
    skipping_planning = True
    planning_prefixes = (
        "i need to ",
        "let me ",
        "i should ",
        "i will ",
        "first, i need to",
        "to answer this, i will",
        "as an ai,",
        "i must follow the guardrails",
        "based on the instructions,",
        "based on my instructions,",
        "the user is asking",
        "analyze user input",
        "determine the appropriate",
        "- user asks:",
        "- context:",
    )
    for line in lines:
        stripped = line.strip().lower()
        if skipping_planning:
            # Check if line looks like numbered planning (e.g. "1. **Analyze...", "2. **Identify...", "3. **Draft...")
            if re.match(r"^\d+\.\s*\*\*(?:analyze|identify|determine|review|understand|formulate|extract|plan|draft|structure)", stripped):
                continue
            if re.match(r"^\d+\.\s*(?:analyze|identify|determine|review|understand|formulate|extract|plan|draft|structure)", stripped):
                continue
            if re.match(r"^\*\*(?:analyze|identify|determine|review|understand|formulate|extract|plan|draft|structure)", stripped):
                continue
            # Skip lines that are purely internal planning
            if any(stripped.startswith(prefix) for prefix in planning_prefixes) and not (
                stripped.startswith("let me help") or stripped.startswith("let's break down") or stripped.startswith("let's look at")
            ):
                continue
            if not line.strip():
                continue
            skipping_planning = False
        cleaned_lines.append(line)

    # 6. Filter out raw safety classifier / guardrail outputs (e.g. Nemotron-Safety / Llama-Guard classifications)
    if re.search(r"^(?:User Safety|Response Safety|Safety Categories|Safety Evaluation|Model Safety):", text, re.IGNORECASE | re.MULTILINE):
        return ""

    cleaned_text = "\n".join(cleaned_lines).strip()
    return cleaned_text if cleaned_text else text.strip()


class OpenRouterAuthError(RuntimeError):
    """Raised when the OpenRouter API key is missing or invalid."""
    pass


class OpenRouterAPIError(RuntimeError):
    """Raised when the OpenRouter API encounters an HTTP or server error."""
    pass


class OpenRouterClient:
    """
    Real OpenRouter API Client for FinWise AI Intelligent Agent.
    Executes actual network requests to OpenRouter's chat completions endpoint.
    Supports OpenRouter Free Models Router ('openrouter/free') with automatic free model selection.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: Optional[str] = None,
        base_url: Optional[str] = None,
        site_url: str = "https://github.com/Anshu666666/finwise",
        site_name: str = "FinWise AI Financial Advisory",
        timeout: Optional[float] = None,
    ):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "") if api_key is None else api_key
        self.default_model = default_model or os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
        self.base_url = base_url or os.getenv("OPENROUTER_BASE_URL", DEFAULT_BASE_URL)
        self.site_url = site_url
        self.site_name = site_name
        self.timeout = timeout or float(os.getenv("OPENROUTER_TIMEOUT", str(DEFAULT_TIMEOUT)))
        self.last_model_used: Optional[str] = None

    @property
    def has_api_key(self) -> bool:
        """Checks if an API key is configured."""
        return bool(self.api_key and len(self.api_key.strip()) > 5 and not self.api_key.startswith("your_openrouter_api_key"))

    def _get_headers(self) -> Dict[str, str]:
        if not self.has_api_key:
            raise OpenRouterAuthError(
                "OPENROUTER_API_KEY is not configured. Please set OPENROUTER_API_KEY in your .env file or environment."
            )

        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key.strip()}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
        }

    def _get_candidate_models(self, requested_model: str) -> List[str]:
        if requested_model in ("openrouter/free", "free"):
            return ["openrouter/free", "openrouter/free", "openrouter/free", "openrouter/free", "openrouter/free"]
        return [requested_model]

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1500,
        max_retries: int = 4,
    ) -> str:
        """
        Executes a REAL synchronous Chat Completion via the OpenRouter API.
        """
        if not self.has_api_key:
            raise OpenRouterAuthError(
                "OPENROUTER_API_KEY is missing. Configure a valid key in .env to perform live LLM requests."
            )

        requested_model = model or self.default_model
        candidate_models = self._get_candidate_models(requested_model)
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        last_exception: Optional[Exception] = None

        for attempt in range(max_retries):
            current_model = candidate_models[attempt % len(candidate_models)]
            payload = {
                "model": current_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(
                        url,
                        headers=self._get_headers(),
                        json=payload,
                    )

                    if response.status_code == 401:
                        raise OpenRouterAuthError(
                            "OpenRouter authentication failed (401 Unauthorized). Check your OPENROUTER_API_KEY."
                        )
                    elif response.status_code in (400, 404, 429, 500, 502, 503, 504) and attempt < max_retries - 1:
                        time.sleep(1.0 * (attempt + 1))
                        continue

                    response.raise_for_status()
                    data = response.json()
                    self.last_model_used = data.get("model", current_model)
                    logger.info(f"OpenRouter response received. Model selected: {self.last_model_used}")

                    message_obj = data["choices"][0].get("message", {})
                    raw_content = message_obj.get("content")
                    if raw_content is None and isinstance(message_obj.get("text"), str):
                        raw_content = message_obj.get("text")

                    content = clean_llm_response(raw_content)

                    if not content:
                        if attempt < max_retries - 1:
                            logger.warning(f"OpenRouter model ({self.last_model_used}) returned empty content. Retrying next candidate...")
                            time.sleep(1.0)
                            continue
                        raise OpenRouterAPIError(f"OpenRouter model ({self.last_model_used}) returned empty content.")

                    return content

            except httpx.HTTPStatusError as e:
                last_exception = OpenRouterAPIError(
                    f"OpenRouter API HTTP error [{e.response.status_code}]: {e.response.text}"
                )
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (attempt + 1))
                    continue
                raise last_exception from e
            except httpx.RequestError as e:
                last_exception = OpenRouterAPIError(f"OpenRouter network connection failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (attempt + 1))
                    continue
                raise last_exception from e

        if last_exception:
            raise last_exception
        raise OpenRouterAPIError("OpenRouter chat completion failed after retries.")

    async def chat_completion_async(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1500,
        max_retries: int = 4,
    ) -> str:
        """
        Executes a REAL asynchronous Chat Completion via the OpenRouter API.
        """
        if not self.has_api_key:
            raise OpenRouterAuthError(
                "OPENROUTER_API_KEY is missing. Configure a valid key in .env to perform live LLM requests."
            )

        import asyncio

        requested_model = model or self.default_model
        candidate_models = self._get_candidate_models(requested_model)
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        last_exception: Optional[Exception] = None

        for attempt in range(max_retries):
            current_model = candidate_models[attempt % len(candidate_models)]
            payload = {
                "model": current_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        url,
                        headers=self._get_headers(),
                        json=payload,
                    )

                    if response.status_code == 401:
                        raise OpenRouterAuthError(
                            "OpenRouter authentication failed (401 Unauthorized). Check your OPENROUTER_API_KEY."
                        )
                    elif response.status_code in (400, 404, 429, 500, 502, 503, 504) and attempt < max_retries - 1:
                        wait_time = 1.0 * (attempt + 1)
                        logger.warning(
                            f"OpenRouter async status {response.status_code} on '{current_model}'. "
                            f"Retrying next candidate in {wait_time}s..."
                        )
                        await asyncio.sleep(wait_time)
                        continue

                    response.raise_for_status()
                    data = response.json()
                    self.last_model_used = data.get("model", current_model)
                    logger.info(f"OpenRouter async response received. Model selected: {self.last_model_used}")

                    message_obj = data["choices"][0].get("message", {})
                    raw_content = message_obj.get("content")
                    if raw_content is None and isinstance(message_obj.get("text"), str):
                        raw_content = message_obj.get("text")

                    content = clean_llm_response(raw_content)

                    if not content:
                        if attempt < max_retries - 1:
                            logger.warning(f"OpenRouter model ({self.last_model_used}) returned empty content. Retrying next candidate...")
                            await asyncio.sleep(1.0)
                            continue
                        raise OpenRouterAPIError(f"OpenRouter async model ({self.last_model_used}) returned empty content.")

                    return content

            except httpx.HTTPStatusError as e:
                last_exception = OpenRouterAPIError(
                    f"OpenRouter async HTTP error [{e.response.status_code}]: {e.response.text}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(1.0 * (attempt + 1))
                    continue
                raise last_exception from e
            except httpx.RequestError as e:
                last_exception = OpenRouterAPIError(f"OpenRouter async connection failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1.0 * (attempt + 1))
                    continue
                raise last_exception from e

        if last_exception:
            raise last_exception
        raise OpenRouterAPIError("OpenRouter async chat completion failed after retries.")

    def test_connection(self) -> Dict[str, Any]:
        """
        Runs a minimal test prompt against OpenRouter to verify credentials and connectivity.
        """
        if not self.has_api_key:
            return {
                "status": "error",
                "message": "OPENROUTER_API_KEY is not set.",
                "connected": False,
            }

        try:
            prompt = [{"role": "user", "content": "Respond with 'OK' only."}]
            response = self.chat_completion(
                messages=prompt,
                max_tokens=10,
                max_retries=2,
            )
            return {
                "status": "success",
                "connected": True,
                "model_used": self.last_model_used or self.default_model,
                "response": response,
            }
        except OpenRouterAuthError as e:
            return {
                "status": "auth_error",
                "connected": False,
                "message": str(e),
            }
        except Exception as e:
            return {
                "status": "error",
                "connected": False,
                "message": str(e),
            }
