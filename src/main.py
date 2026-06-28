from src.scrapers.boulanger import BoulangerScraper
from src.state import StateStore
from src.compare import has_changed
from src.notify import Notifier
import os


def main():

    product = {
        "id": "midea-portasplit",
        "name": "Midea PortaSplit",
    }

    scraper = BoulangerScraper()

    result = scraper.check(product)

    store = StateStore()
    state = store.load()

    old = state.get(product["id"])

    changed, reason = has_changed(old, result.__dict__)

    print("Result:", result)
    print("Changed:", changed, reason)

    # 🔥 EMAIL NOTIFIER (GitHub Secrets)
    notifier = None

    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    email_to = os.getenv("EMAIL_TO")

    if email_user and email_pass and email_to:
        notifier = Notifier(
            email_from=email_user,
            email_to=email_to,
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            password=email_pass
        )

    if changed:

        print("🔥 CHANGE DETECTED")

        state[product["id"]] = result.to_dict() if hasattr(result, "to_dict") else result.__dict__

        # fix datetime if needed
        if "checked_at" in state[product["id"]] and hasattr(state[product["id"]]["checked_at"], "isoformat"):
            state[product["id"]]["checked_at"] = state[product["id"]]["checked_at"].isoformat()

        store.save(state)

        # 🔔 EMAIL ALERT
        if notifier:

            subject = f"[Stock Alert] {product['name']}"

            message = f"""
Produit : {product['name']}
Changement détecté : {reason}

Disponible : {getattr(result, 'available', None)}
Prix : {getattr(result, 'price', None)}

URL : {getattr(result, 'url', '')}
"""

            notifier.send(subject, message)

    else:
        print("No change detected")


if __name__ == "__main__":
    main()