from src.browser import Browser
from src.extractor import extract_json_ld
from src.product_parser import parse_product
from src.search import SearchEngine
from src.finders.boulanger_finder import BoulangerFinder
from src.robust_extractor import RobustExtractor


class BoulangerScraper:

    def __init__(self):

        self.search_engine = SearchEngine(
            base_url="https://www.boulanger.com",
            search_path="/resultats?tr={query}"
        )

        self.finder = BoulangerFinder()

    def check(self, product):

        # 1. Search page
        search_html = self.search_engine.search(product["name"])

        result = self.finder.find(search_html, product["name"])

        if not result:
            return None

        # 2. Product page
        with Browser() as browser:

            page = browser.new_page()
            page.goto(result["url"], timeout=60000)

            html = page.content()

        extractor = RobustExtractor()

        data = extractor.extract(html)

        return parse_product(
            json_ld_list=[],
            retailer="boulanger",
            url=result["url"],
            product_id=product["id"],
            product_name=product["name"]
        ). __class__(
            product_id=product["id"],
            product_name=product["name"],
            retailer="boulanger",
            url=result["url"],
            available=data["available"],
            price=float(data["price"]) if data["price"] else None,
            message="",
        )