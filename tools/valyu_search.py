# tools/valyu_search.py
from langchain_core.tools import tool
from typing import List, Dict
import requests
import os

@tool
def valyu_search(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search using Valyu AI for insurance-related information.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of search results with title, snippet, and URL
    """
    
    # Get Valyu API credentials from environment
    api_key = os.getenv("VALYU_API_KEY")
    api_url = os.getenv("VALYU_API_URL", "https://api.valyu.ai/search")
    
    if not api_key:
        print("⚠️  Valyu API key not found in environment")
        # Return mock data for development
        return [
            {
                "title": f"Mock result for: {query}",
                "snippet": "This is mock data. Configure VALYU_API_KEY to use real search.",
                "url": "https://example.com",
                "relevance_score": 0.9
            }
        ]
    
    try:
        # Make API request to Valyu
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": query,
            "max_results": max_results
        }
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        results = response.json().get("results", [])
        
        print(f"🔍 Valyu Search: Found {len(results)} results for '{query}'")
        
        return results
        
    except Exception as e:
        print(f"❌ Valyu search failed: {e}")
        # Return empty results on error
        return []


@tool
def valyu_insurance_policy_search(policy_type: str, coverage_details: str) -> Dict:
    """
    Perform a specialized insurance policy search using the Valyu API.

    Args:
        policy_type: Type of insurance (e.g., 'Auto', 'Health').
        coverage_details: Details about desired policy coverage.

    Returns:
        A dictionary summarizing the search query and API results.
    """
    query = f"{policy_type} insurance policy {coverage_details}"
    results = valyu_search.invoke({"query": query, "max_results": 3})
    return {
        "policy_type": policy_type,
        "search_query": query,
        "results": results,
        "result_count": len(results)
    }


class ValyuSearchAgent:
    def __init__(self, name: str = "ValyuSearchAgent"):
        self.name = name
        self.search_history = []

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        print(f"\n🔍 [{self.name}] Searching: {query}")

        results = valyu_search.invoke({
            "query": query,
            "max_results": max_results
        })

        self.search_history.append({
            "query": query,
            "results_count": len(results),
            "timestamp": str(os.times())
        })

        return results

    def get_search_summary(self) -> Dict:
        return {
            "total_searches": len(self.search_history),
            "searches": self.search_history
        }