from sources.browser import Browser, create_driver
from config.settings import settings

class BrowserExtension:
    def __init__(self):
        # Initialize browser on demand or keep persistent?
        # For now, we'll create a new instance per command or manage a singleton in InteractionService
        # Ideally, we should reuse the browser instance from InteractionService
        self.commands = {
            "browse_website": self.browse_website
        }

    def browse_website(self, url: str):
        """
        Visits a website and extracts its content.
        Args:
            url: The URL to visit.
        """
        # Note: In a real implementation, we'd want to access the shared browser instance
        # For this wrapper, we'll assume we can get it or create a temporary one
        driver = create_driver(headless=True)
        browser = Browser(driver)
        try:
            browser.browse(url)
            return browser.get_text_content()
        finally:
            browser.close()
