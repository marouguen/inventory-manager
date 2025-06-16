from sqlalchemy.orm import Session
from app.models.stock import StockMovement
from app.schemas.stock import StockMovementCreate
from app.models.product import Product
from fastapi import HTTPException

def create_stock_movement(db: Session, movement: StockMovementCreate, user_id: int):
    # Get product
    product = db.query(Product).filter(Product.id == movement.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update stock
    if movement.type == "in":
        product.quantity += movement.quantity
    elif movement.type == "out":
        if product.quantity < movement.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        product.quantity -= movement.quantity

    # Create log
    log = StockMovement(**movement.dict(), user_id=user_id)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_stock_logs(db: Session, skip=0, limit=100):
    return db.query(StockMovement).order_by(StockMovement.timestamp.desc()).offset(skip).limit(limit).all()
