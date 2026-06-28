from src.utils.score import score_title
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class DartyFinder:

    BASE_URL = "https://www.darty.com"

    def find(self, html: str, query: str):

        soup = BeautifulSoup(html, "lxml")

        links = soup.select("a[href*='produit']")

        candidates = []

        for link in links:

            href = link.get("href")
            title = link.get_text(" ", strip=True)

            if not href or len(title) < 5:
                continue

            score = score_title(title, query)

            if score <= 0:
                continue

            candidates.append({
                "title": title,
                "url": urljoin(self.BASE_URL, href),
                "score": score
            })

        if not candidates:
            return None

        return max(candidates, key=lambda x: x["score"])