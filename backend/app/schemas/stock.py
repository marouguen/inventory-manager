from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class StockMovementBase(BaseModel):
    product_id: int
    quantity: float
    type: Literal["in", "out"]

class StockMovementCreate(StockMovementBase):
    pass

class StockMovementOut(StockMovementBase):
    id: int
    user_id: int
    timestamp: datetime

    class ConfigDict:
        orm_mode = True
