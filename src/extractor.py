import json
from bs4 import BeautifulSoup


def extract_json_ld(html: str):
    """
    Extrait tous les blocs JSON-LD d'une page HTML
    """
    soup = BeautifulSoup(html, "lxml")

    scripts = soup.find_all("script", type="application/ld+json")

    data = []

    for script in scripts:
        try:
            content = script.string
            if not content:
                continue

            parsed = json.loads(content)

            # Certains sites mettent une liste
            if isinstance(parsed, list):
                data.extend(parsed)
            else:
                data.append(parsed)

        except Exception:
            continue

    return data