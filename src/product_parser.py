from src.models import ProductStatus
from datetime import datetime


def parse_product(json_ld_list, retailer: str, url: str, product_id: str, product_name: str):

    for item in json_ld_list:

        if isinstance(item, dict) and item.get("@type") in ["Product", "Offer", "ProductGroup"]:

            offers = item.get("offers", {})

            # Cas liste
            if isinstance(offers, list):
                offers = offers[0]

            availability = offers.get("availability", "")

            in_stock = "InStock" in availability

            price = offers.get("price")

            try:
                price = float(price) if price else None
            except:
                price = None

            return ProductStatus(
                product_id=product_id,
                product_name=product_name,
                retailer=retailer,
                url=url,
                available=in_stock,
                price=price,
                message=availability,
                checked_at=datetime.utcnow()
            )

    return ProductStatus(
        product_id=product_id,
        product_name=product_name,
        retailer=retailer,
        url=url,
        available=False,
        price=None,
        message="No JSON-LD found",
        checked_at=datetime.utcnow()
    )