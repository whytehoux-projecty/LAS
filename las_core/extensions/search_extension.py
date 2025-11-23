from sources.tools.web_search import WebSearchTool
from config.settings import settings

class SearchExtension:
    def __init__(self):
        # Initialize the underlying tool
        self.tool = WebSearchTool(searxng_url=settings.searxng_base_url if hasattr(settings, 'searxng_base_url') else "http://localhost:8080")
        
        # Define commands exposed by this extension
        self.commands = {
            "web_search": self.web_search
        }

    def web_search(self, query: str, num_results: int = 5):
        """
        Performs a web search using SearXNG.
        Args:
            query: The search query.
            num_results: Number of results to return.
        """
        return self.tool.search(query, num_results)
