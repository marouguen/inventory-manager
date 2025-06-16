from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class StockLog(Base):
    __tablename__ = "stock_logs"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)  # "in" or "out"
    quantity = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
