from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.deps import get_current_user
from app.crud import product as crud
from datetime import date

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/by-category")
def stock_by_category(
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    print("Received dates:", start_date, end_date)
    return crud.get_stock_by_category(db, start_date, end_date)

@router.get("/top-products")
def top_products(
    limit: int = 5,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    print("Received dates:", start_date, end_date)
    return crud.get_top_products_by_quantity(db, start_date, end_date, limit)
