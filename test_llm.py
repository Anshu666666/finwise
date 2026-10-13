import os
import sys

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dotenv import load_dotenv

# Load environment variables from existing .env
load_dotenv()

from agent.financial_agent import default_agent
from agent.openrouter_client import OpenRouterClient, DEFAULT_MODEL


def main():
    configured_model = os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
    print("=" * 70)
    print("FINWISE AI – OPENROUTER FREE MODELS ROUTER TESTER")
    print(f"Target Model Config: {configured_model}")
    print("Endpoint: https://openrouter.ai/api/v1/chat/completions")
    print("=" * 70)

    client = OpenRouterClient()
    agent = default_agent.pydantic_agent

    print("\nEnter your query to test OpenRouter inference.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("User Query > ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        cleaned_input = user_input.strip()

        if cleaned_input.lower() == "exit":
            print("Exiting...")
            break

        if not cleaned_input:
            continue

        print("\n[OpenRouter Free Router] Sending request...")
        try:
            # First try direct client to inspect selected free model
            messages = [{"role": "user", "content": cleaned_input}]
            response_text = client.chat_completion(messages=messages, model=configured_model)
            model_used = client.last_model_used or configured_model

            print(f"\n✓ Response received from OpenRouter!")
            print(f"Model used: {model_used}")
            print(f"\n--- Output ---\n{response_text}\n" + "-" * 70 + "\n")
        except Exception as e:
            print(f"\nDirect OpenRouter request error: {e}")
            print("Retrying through PydanticAI agent...")
            try:
                result = agent.run_sync(cleaned_input)
                response_text = (
                    result.output
                    if hasattr(result, "output") and result.output is not None
                    else getattr(result, "data", str(result))
                )
                print(f"\n--- PydanticAI Agent Output ---\n{response_text}\n" + "-" * 70 + "\n")
            except Exception as agent_err:
                print(f"\nLLM request failed.\nError: {agent_err}\n")


if __name__ == "__main__":
    main()
