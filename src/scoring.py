import re


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def score_product(title: str, query: str) -> float:

    t = normalize(title)
    q = normalize(query)

    score = 0.0

    # 1. correspondance directe
    if q in t:
        score += 10

    # 2. mots communs
    for word in query.lower().split():
        if normalize(word) in t:
            score += 2

    # 3. bonus si titre long (souvent produit complet)
    if len(title) > 20:
        score += 1

    return score