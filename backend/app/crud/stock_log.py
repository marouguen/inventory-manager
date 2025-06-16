from sqlalchemy.orm import Session
from app.models.stock_log import StockLog
from app.models.product import Product
from app.schemas.stock_log import StockLogCreate
from fastapi import HTTPException
import csv
import io
from datetime import datetime
from fastapi.responses import StreamingResponse
from app.models.stock_log import StockLog
from sqlalchemy import func
from app.models.product import Product
from datetime import datetime
from sqlalchemy import func, extract

def export_logs_csv(
    db: Session,
    product_id: int = None,
    type: str = None,
    start_date: str = None,
    end_date: str = None,
):
    query = db.query(StockLog)

    if product_id:
        query = query.filter(StockLog.product_id == product_id)
    if type:
        query = query.filter(StockLog.type == type)
    if start_date:
        query = query.filter(StockLog.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(StockLog.timestamp <= datetime.fromisoformat(end_date))

    logs = query.order_by(StockLog.timestamp.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["id", "product_id", "user_id", "type", "quantity", "timestamp"])

    for log in logs:
        writer.writerow([
            log.id,
            log.product_id,
            log.user_id,
            log.type,
            log.quantity,
            log.timestamp.isoformat()
        ])

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=stock_logs.csv"}
    )

def create_log(db: Session, data: StockLogCreate, user_id: int):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.type == "in":
        product.quantity += data.quantity
    elif data.type == "out":
        if product.quantity < data.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        product.quantity -= data.quantity

    log = StockLog(
        product_id=data.product_id,
        quantity=data.quantity,
        type=data.type,
        user_id=user_id,
    )

    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_logs(db: Session, product_id: int = None, type: str = None, skip: int = 0, limit: int = 50):
    query = db.query(StockLog)
    if product_id:
        query = query.filter(StockLog.product_id == product_id)
    if type:
        query = query.filter(StockLog.type == type)
    return query.order_by(StockLog.timestamp.desc()).offset(skip).limit(limit).all()

def get_top_moved_products(db: Session, limit: int = 5):
    result = (
        db.query(
            Product.id,
            Product.name,
            func.count(StockLog.id).label("movement_count")
        )
        .join(StockLog, StockLog.product_id == Product.id)
        .group_by(Product.id)
        .order_by(func.count(StockLog.id).desc())
        .limit(limit)
        .all()
    )
    return [{"id": r.id, "name": r.name, "count": r.movement_count} for r in result]

def get_summary_metrics(db: Session):
    # Get current month and year
    now = datetime.utcnow()
    year = now.year
    month = now.month

    # Total stock-in this month
    stock_in = (
        db.query(func.coalesce(func.sum(StockLog.quantity), 0))
        .filter(StockLog.type == "in")
        .filter(extract("year", StockLog.timestamp) == year)
        .filter(extract("month", StockLog.timestamp) == month)
        .scalar()
    )

    # Total stock-out this month
    stock_out = (
        db.query(func.coalesce(func.sum(StockLog.quantity), 0))
        .filter(StockLog.type == "out")
        .filter(extract("year", StockLog.timestamp) == year)
        .filter(extract("month", StockLog.timestamp) == month)
        .scalar()
    )

    # Total product count
    from app.models.product import Product
    total_products = db.query(func.count(Product.id)).scalar()

    return {
        "total_products": total_products,
        "stock_in_this_month": float(stock_in),
        "stock_out_this_month": float(stock_out),
    }