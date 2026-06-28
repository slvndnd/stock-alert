from src.scrapers.boulanger import BoulangerScraper
from src.scrapers.darty import DartyScraper
from src.scrapers.leroymerlin import LeroyMerlinScraper


def main():

    product = {
        "id": "midea-portasplit",
        "name": "Midea PortaSplit"
    }

    scrapers = [
        BoulangerScraper(),
        DartyScraper(),
        LeroyMerlinScraper(),
    ]

    results = []

    for scraper in scrapers:

        try:
            res = scraper.check(product)
            if res:
                results.append(res)
        except Exception as e:
            print(f"{scraper.__class__.__name__} error:", e)

    print("\nRESULTS:")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()