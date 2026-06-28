from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src.utils.score import score_title


class LeroyMerlinFinder:

    BASE_URL = "https://www.leroymerlin.fr"

    def find(self, html: str, query: str):

        soup = BeautifulSoup(html, "lxml")

        # Leroy Merlin structure assez stable
        links = soup.select("a[href*='/produits/']")

        candidates = []

        for link in links:

            href = link.get("href")
            title = link.get_text(" ", strip=True)

            if not href:
                continue

            score = score_title(title, query)

            if score == 0:
                continue

            candidates.append({
                "title": title,
                "url": urljoin(self.BASE_URL, href),
                "score": score
            })

        if not candidates:
            return None

        return max(candidates, key=lambda x: x.get("score", 0))