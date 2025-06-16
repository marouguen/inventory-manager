from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class StockLogBase(BaseModel):
    product_id: int
    quantity: float
    type: Literal["in", "out"]

class StockLogCreate(StockLogBase):
    pass

class StockLogOut(StockLogBase):
    id: int
    user_id: int
    timestamp: datetime

    class ConfigDict:
        from_attributes = True
