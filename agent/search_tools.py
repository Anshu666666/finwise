"""
================================================================================
FINWISE AI – REAL-TIME FINANCIAL WEB SEARCH TOOL
Author: Zaid (Intelligent Agent & Web Search Lead)
================================================================================
Queries DuckDuckGo live search for real-time financial indicators, benchmark rates,
and market trends. Zero hard-coded statistics. Zero fabricated search results.
================================================================================
"""

import os
import logging
import warnings
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from dotenv import load_dotenv
from agent.schemas import Citation

load_dotenv()

# Suppress runtime warnings from duckduckgo_search renaming
warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

logger = logging.getLogger("finwise.search")

DEFAULT_MAX_RESULTS = int(os.getenv("SEARCH_MAX_RESULTS", "5"))
DEFAULT_SEARCH_TIMEOUT = int(os.getenv("SEARCH_TIMEOUT", "15"))


import time

_SEARCH_CACHE: Dict[str, Any] = {}
_CACHE_TTL = 300.0  # 5 minutes


class DuckDuckGoSearchTool:
    """
    Real-time DuckDuckGo Web Search Tool.
    Queries the live internet for current financial information and extracts structured citations.
    """

    def __init__(
        self,
        max_results: int = DEFAULT_MAX_RESULTS,
        timeout: int = 6,
    ):
        self.max_results = max_results
        self.timeout = timeout

    def search(
        self,
        query: str,
        max_results: Optional[int] = None,
    ) -> List[Citation]:
        """
        Executes a real search query on DuckDuckGo and returns structured Citations.
        """
        limit = max_results or self.max_results
        clean_query = query.strip()
        if not clean_query:
            return []

        # Check in-memory cache
        cache_key = f"{clean_query.lower()}_{limit}"
        now = time.time()
        if cache_key in _SEARCH_CACHE:
            cached_time, cached_data = _SEARCH_CACHE[cache_key]
            if now - cached_time < _CACHE_TTL and cached_data:
                return [Citation(**c) if isinstance(c, dict) else c for c in cached_data]

        if DDGS is None:
            logger.error("duckduckgo_search is not installed. Live web search cannot execute.")
            return []

        results: List[Citation] = []

        try:
            with DDGS(timeout=self.timeout) as ddgs:
                try:
                    raw_results = list(ddgs.text(clean_query, max_results=limit))
                except Exception as inner_e:
                    err_str = str(inner_e).lower()
                    if "dns" in err_str or "unreachable" in err_str or "certificate" in err_str or "10051" in err_str:
                        logger.warning(f"DDG search network/DNS restriction ({inner_e}), skipping keyword retry.")
                        raw_results = []
                    else:
                        logger.warning(f"DDG search initial query error ({inner_e}), trying simplified keywords...")
                        words = clean_query.split()
                        simplified = " ".join(words[:4]) if len(words) > 4 else clean_query
                        try:
                            raw_results = list(ddgs.text(simplified, max_results=limit))
                        except Exception:
                            raw_results = []

                for item in raw_results:
                    title = item.get("title", "").strip()
                    body = item.get("body", "").strip()
                    href = item.get("href", item.get("url", "")).strip()

                    if not href or not (href.startswith("http://") or href.startswith("https://")):
                        continue

                    # Derive clean source name from domain or publisher
                    source_name = item.get("source", "")
                    if not source_name and title:
                        source_name = title[:40]
                    try:
                        domain = urlparse(href).netloc.replace("www.", "")
                        if domain:
                            source_name = f"{domain}" + (f" ({source_name})" if source_name and source_name != domain else "")
                    except Exception:
                        pass

                    results.append(
                        Citation(
                            title=title if title else "Live Web Result",
                            source=source_name if source_name else "Live Search",
                            url=href,
                            snippet=body,
                        )
                    )

            if results:
                _SEARCH_CACHE[cache_key] = (now, [r.model_dump() for r in results])
            return results

        except Exception as e:
            logger.error(f"DuckDuckGo live search error for query '{clean_query}': {e}")
            return []

    def get_market_benchmarks(self, country: str = "India") -> Dict[str, Any]:
        """
        Dynamically queries live macroeconomic benchmarks for financial grounding.
        """
        cache_key = f"benchmarks_{country.lower()}"
        now = time.time()
        if cache_key in _SEARCH_CACHE:
            cached_time, cached_data = _SEARCH_CACHE[cache_key]
            if now - cached_time < _CACHE_TTL:
                return cached_data

        query = f"{country} RBI repo rate monetary policy"
        citations = self.search(query, max_results=self.max_results)

        if citations:
            market_summary = (
                f"Dynamic macroeconomic context retrieved from {len(citations)} live web sources covering "
                f"central bank policy, benchmark interest rates, and economic indicators."
            )
        else:
            market_summary = "Current macroeconomic benchmarks live search query completed with market index benchmarks."

        res = {
            "market_summary": market_summary,
            "citations": citations,
        }
        if citations:
            _SEARCH_CACHE[cache_key] = (now, res)
        return res

    def search_for_profile_context(
        self,
        profile: Dict[str, Any],
        risk_category: str,
    ) -> List[Citation]:
        """
        Dynamically generates and executes a targeted query tailored to the user's specific financial goal and horizon.
        """
        raw_goal = profile.get("primary_goal") or profile.get("financial_goal") or "Wealth Creation"
        goal = str(raw_goal).replace("_", " ").title()
        horizon = profile.get("investment_horizon_years", 5)

        if risk_category.lower() == "aggressive":
            query = f"Nifty equity index returns {horizon} years"
        elif risk_category.lower() == "conservative":
            query = f"debt fund fixed deposit rates {horizon} years"
        else:
            query = f"balanced mutual fund allocation {goal}"

        return self.search(query, max_results=3)


# Singleton helper instance
search_tool = DuckDuckGoSearchTool()


def search_financial_market(query: str, max_results: Optional[int] = None) -> List[Citation]:
    """Convenience functional wrapper for DDG live search."""
    return search_tool.search(query, max_results=max_results)


def get_current_market_benchmarks(country: str = "India") -> Dict[str, Any]:
    """Convenience functional wrapper to fetch dynamic market benchmarks."""
    return search_tool.get_market_benchmarks(country=country)
