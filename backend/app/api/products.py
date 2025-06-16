from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.crud import product as crud
from app.deps import get_current_user, require_admin
from fastapi.responses import StreamingResponse


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db), user = Depends(require_admin)):
    return crud.create_product(db, product)

@router.get("/", response_model=List[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 2000,
    name: str = None,
    barcode: str = None,
    category_id: int = None,
    supplier_id: int = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return crud.get_products(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        barcode=barcode,
        category_id=category_id,
        supplier_id=supplier_id
    )

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, update: ProductUpdate, db: Session = Depends(get_db), user = Depends(require_admin)):
    product = crud.update_product(db, product_id, update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), user = Depends(require_admin)):
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": f"Deleted product {product.name}"}

@router.get("/export")
def export_products_csv(
    name: str = None,
    barcode: str = None,
    category_id: int = None,
    supplier_id: int = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return crud.export_products_csv(
        db=db,
        name=name,
        barcode=barcode,
        category_id=category_id,
        supplier_id=supplier_id,
    )

@router.get("/low-stock", response_model=List[ProductOut])
def low_stock(threshold: float = 10.0, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_low_stock_products(db, threshold)
