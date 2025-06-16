from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import SessionLocal
from app.schemas.stock_log import StockLogCreate, StockLogOut
from app.crud import stock_log as crud
from app.deps import get_current_user
from fastapi.responses import StreamingResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/in", response_model=StockLogOut)
def stock_in(data: StockLogCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if data.type != "in":
        raise ValueError("Use 'in' type only for this endpoint.")
    return crud.create_log(db, data, user_id=user.id)

@router.post("/out", response_model=StockLogOut)
def stock_out(data: StockLogCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if data.type != "out":
        raise ValueError("Use 'out' type only for this endpoint.")
    return crud.create_log(db, data, user_id=user.id)

@router.get("/logs", response_model=List[StockLogOut])
def list_logs(
    product_id: Optional[int] = None,
    type: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return crud.get_logs(db, product_id, type, skip, limit)

@router.get("/export")
def export_logs_csv(
    product_id: Optional[int] = None,
    type: Optional[str] = None,
    start_date: Optional[str] = None,  # ISO format e.g. "2024-01-01"
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return crud.export_logs_csv(
        db,
        product_id=product_id,
        type=type,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/top-moved")
def top_moved_products(limit: int = 5, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_top_moved_products(db, limit)

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_summary_metrics(db)
