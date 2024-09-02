from typing import Optional
from pydantic import BaseModel
from enum import Enum


class Tier(str, Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    TOP_PREMIUM = "top_premium"


class CreateEbook(BaseModel):
    topic: str
    target_audience: str
    tier: Optional[Tier] = None
