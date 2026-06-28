from playwright.sync_api import sync_playwright


class SearchEngine:

    def __init__(self, base_url, search_path):
        self.base_url = base_url
        self.search_path = search_path

    def search(self, query: str):

        url = self.base_url + self.search_path.format(query=query)

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            # 🔥 timeout global plus large
            page.set_default_timeout(60000)

            page.goto(url, wait_until="domcontentloaded")

            # 🔥 on attend juste que le JS ait eu le temps de rendre
            page.wait_for_timeout(4000)

            html = page.content()

            browser.close()

            return html