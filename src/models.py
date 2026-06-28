from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ProductStatus:
    product_id: str
    product_name: str

    retailer: str

    url: str

    available: bool

    price: Optional[float]

    currency: str = "EUR"

    message: str = ""

    checked_at: datetime = datetime.utcnow()

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "retailer": self.retailer,
            "url": self.url,
            "available": self.available,
            "price": self.price,
            "currency": self.currency,
            "message": self.message,
            "checked_at": self.checked_at.isoformat()
        }