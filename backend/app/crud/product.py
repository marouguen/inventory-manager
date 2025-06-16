from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
import csv
import io
from fastapi.responses import StreamingResponse
from app.models.category import Category
from sqlalchemy import func, and_, cast, Date
from app.models.stock_log import StockLog
from datetime import date

def export_products_csv(
    db: Session,
    name: str = None,
    barcode: str = None,
    category_id: int = None,
    supplier_id: int = None,
):
    query = db.query(Product)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if barcode:
        query = query.filter(Product.barcode == barcode)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if supplier_id:
        query = query.filter(Product.supplier_id == supplier_id)

    products = query.all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["id", "name", "sku", "barcode", "quantity", "unit", "category_id", "supplier_id"])

    # Write rows
    for p in products:
        writer.writerow([
            p.id, p.name, p.sku, p.barcode, p.quantity, p.unit, p.category_id, p.supplier_id
        ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=products.csv"})

def create_product(db: Session, product_in: ProductCreate):
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: str = None,
    barcode: str = None,
    category_id: int = None,
    supplier_id: int = None
):
    query = db.query(Product)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if barcode:
        query = query.filter(Product.barcode == barcode)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if supplier_id:
        query = query.filter(Product.supplier_id == supplier_id)

    return query.offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product_in: ProductUpdate):
    product = get_product(db, product_id)
    if not product:
        return None
    for field, value in product_in.model_dump().items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product

def get_low_stock_products(db: Session, threshold: float = 10.0):
    return db.query(Product).filter(Product.quantity < threshold).all()


def get_stock_by_category(db: Session, start_date: date = None, end_date: date = None):
    query = (
        db.query(
            Category.name.label("category"),
            func.sum(StockLog.quantity).label("total_quantity")
        )
        .join(Product, Product.id == StockLog.product_id)
        .join(Category, Product.category_id == Category.id)
    )

    if start_date and end_date:
        query = query.filter(
            and_(
                cast(StockLog.timestamp, Date) >= start_date,
                cast(StockLog.timestamp, Date) <= end_date
            )
        )

    result = query.group_by(Category.name).order_by(func.sum(StockLog.quantity).desc()).all()

    return [
        {
            "category": row.category,
            "total_quantity": float(row.total_quantity) if row.total_quantity else 0
        }
        for row in result
    ]

def get_top_products_by_quantity(db: Session, start_date: date = None, end_date: date = None, limit: int = 5):
    query = (
        db.query(
            Product.name.label("name"),
            func.sum(StockLog.quantity).label("quantity")
        )
        .join(StockLog, StockLog.product_id == Product.id)
    )

    if start_date and end_date:
        query = query.filter(
            and_(
                cast(StockLog.timestamp, Date) >= start_date,
                cast(StockLog.timestamp, Date) <= end_date
            )
        )

    result = query.group_by(Product.name).order_by(func.sum(StockLog.quantity).desc()).limit(limit).all()

    return [
        {
            "name": row.name,
            "quantity": float(row.quantity) if row.quantity else 0
        }
        for row in result
    ]
