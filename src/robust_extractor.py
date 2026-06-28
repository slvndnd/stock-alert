import json
import re
from bs4 import BeautifulSoup


def safe_json_loads(raw: str):
    """
    Parse JSON-LD de manière tolérante aux erreurs réelles du web
    """

    if not raw:
        return None

    raw = raw.strip()

    # 🔥 suppression caractères invisibles
    raw = raw.replace("\n", " ").replace("\t", " ")

    # 🔥 tentative directe
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # 🔥 fallback : extraire uniquement le premier objet JSON
    try:
        match = re.search(r'\{.*\}', raw)
        if match:
            return json.loads(match.group(0))
    except:
        return None

    return None


class RobustExtractor:

    def extract(self, html: str):

        soup = BeautifulSoup(html, "lxml")

        result = {
            "price": None,
            "available": False,
            "name": None
        }

        scripts = soup.find_all("script", type="application/ld+json")

        for s in scripts:

            data = safe_json_loads(s.string)

            if not data:
                continue

            if isinstance(data, list):
                data = data[0]

            if not isinstance(data, dict):
                continue

            # 🔥 filtre produit uniquement
            if data.get("@type") not in ["Product", "Offer", "ProductGroup"]:
                continue

            offers = data.get("offers", {})

            if isinstance(offers, list):
                offers = offers[0]

            if isinstance(offers, dict):

                price = offers.get("price")
                if price:
                    try:
                        result["price"] = float(price)
                    except:
                        pass

                availability = offers.get("availability", "")
                if "InStock" in availability:
                    result["available"] = True
                elif "OutOfStock" in availability:
                    result["available"] = False

            if data.get("name"):
                result["name"] = data["name"]

        # 🔥 fallback texte brut (ultra important)
        text = soup.get_text(" ", strip=True).lower()

        if any(x in text for x in ["en stock", "disponible", "ajouter au panier"]):
            result["available"] = True

        if any(x in text for x in ["rupture", "indisponible", "épuisé"]):
            result["available"] = False

        return result