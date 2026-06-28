from src.browser import Browser
from src.extractor import extract_json_ld
from src.robust_extractor import RobustExtractor


class BaseScraper:

    def __init__(self, name):
        self.name = name
        self.extractor = RobustExtractor()

    def open_page(self, url):

        with Browser() as browser:
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_timeout(4000)
            return page.content()