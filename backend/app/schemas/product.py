from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    sku: str
    barcode: str
    quantity: float
    unit: str
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class ConfigDict:
        from_attributes = True
