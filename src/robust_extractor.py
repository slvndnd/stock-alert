import json
import re
from bs4 import BeautifulSoup


class RobustExtractor:

    def extract(self, html: str):

        soup = BeautifulSoup(html, "lxml")

        result = {
            "price": None,
            "available": False,
            "name": None
        }

        # ----------------------------
        # 🥇 1. JSON-LD (priorité)
        # ----------------------------
        scripts = soup.find_all("script", type="application/ld+json")

        for s in scripts:

            try:
                if not s.string:
                    continue

                data = json.loads(s.string.strip())

                if isinstance(data, list):
                    data = data[0]

                if not isinstance(data, dict):
                    continue

                if data.get("@type") != "Product":
                    continue

                # name
                if data.get("name"):
                    result["name"] = data["name"]

                offers = data.get("offers")

                if isinstance(offers, list):
                    offers = offers[0]

                if isinstance(offers, dict):

                    price = offers.get("price")
                    if price:
                        try:
                            result["price"] = float(price)
                        except:
                            pass

                    availability = str(offers.get("availability", ""))

                    if "InStock" in availability:
                        result["available"] = True
                    elif "OutOfStock" in availability:
                        result["available"] = False

            except:
                continue

        # ----------------------------
        # 🥈 2. META / MICRODATA fallback
        # ----------------------------

        if not result["price"]:
            meta_price = soup.select_one("meta[property='product:price:amount']")
            if meta_price:
                try:
                    result["price"] = float(meta_price["content"])
                except:
                    pass

        # ----------------------------
        # 🥉 3. TEXT HEURISTICS (IMPORTANT)
        # ----------------------------

        text = soup.get_text(" ", strip=True).lower()

        # disponibilité
        if any(w in text for w in ["en stock", "disponible", "ajouter au panier"]):
            result["available"] = True

        if any(w in text for w in ["rupture", "indisponible", "épuisé"]):
            result["available"] = False

        # ----------------------------
        # 💡 4. PRICE REGEX fallback (TRÈS utile)
        # ----------------------------

        if not result["price"]:
            match = re.search(r"(\d{2,5}[.,]\d{2})\s?€", text)
            if match:
                try:
                    result["price"] = float(match.group(1).replace(",", "."))
                except:
                    pass

        return result