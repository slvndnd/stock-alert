import re


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def score_title(title: str, query: str) -> float:

    t = normalize(title)
    q_words = query.lower().split()

    score = 0.0

    # 1. match global (très important)
    if normalize(query) in t:
        score += 10

    # 2. mots du nom
    for word in q_words:
        if normalize(word) in t:
            score += 2

    # 3. pénalité accessoires / pièces
    bad_words = [
        "accessoire", "filtre", "support", "kit",
        "pièce", "chargeur", "tuyau", "extension"
    ]

    for bw in bad_words:
        if bw in title.lower():
            score -= 5

    # 4. bonus produit principal
    if len(title) > 20:
        score += 1

    return score