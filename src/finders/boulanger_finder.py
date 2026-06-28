from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src.scoring import score_product


class BoulangerFinder:

    BASE_URL = "https://www.boulanger.com"

    def find(self, html: str, query: str):

        soup = BeautifulSoup(html, "lxml")

        links = soup.select("a[href*='/ref/']")

        candidates = []

        for link in links:

            href = link.get("href")
            title = link.get_text(" ", strip=True)

            if not href or len(title) < 5:
                continue

            score = score_product(title, query)

            candidates.append({
                "title": title,
                "url": urljoin(self.BASE_URL, href),
                "score": score
            })

        if not candidates:
            return None

        # 🔥 meilleur score
        best = max(candidates, key=lambda x: x["score"])

        if best["score"] == 0:
            return None

        return best