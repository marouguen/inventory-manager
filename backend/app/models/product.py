from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False, index=True)
    barcode = Column(String, unique=True, nullable=False)
    quantity = Column(Float, default=0)
    unit = Column(String, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
