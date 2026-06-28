from src.search import SearchEngine
from src.finders.leroymerlin import LeroyMerlinFinder
from src.robust_extractor import RobustExtractor
from src.browser import Browser


class LeroyMerlinScraper:

    def __init__(self):

        self.search_engine = SearchEngine(
            base_url="https://www.leroymerlin.fr",
            search_path="/recherche/?q={query}"
        )

        self.finder = LeroyMerlinFinder()
        self.extractor = RobustExtractor()

    def check(self, product):

        html = self.search_engine.search(product["name"])

        result = self.finder.find(html, product["name"])

        if not result:
            return None

        with Browser() as browser:

            page = browser.new_page()
            page.goto(result["url"], timeout=60000)

            html = page.content()

        data = self.extractor.extract(html)

        return {
            "retailer": "leroymerlin",
            "url": result["url"],
            "price": data["price"],
            "available": data["available"],
            "product": product["name"]
        }