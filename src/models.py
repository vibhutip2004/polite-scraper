from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, field_validator

class BookRecord(BaseModel):
    title: str
    product_url: HttpUrl
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: Optional[str] = None
    description: Optional[str] = None
    source_page: HttpUrl
    fetched_at: datetime

    @field_validator("price_gbp")
    @classmethod
    def price_must_be_non_negative(cls, value: float) -> float:
        if value < 0:
            raise ValueError("price_gbp must be >= 0")
        return value