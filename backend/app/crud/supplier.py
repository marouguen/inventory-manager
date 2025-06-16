from sqlalchemy.orm import Session
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate

def create_supplier(db: Session, data: SupplierCreate):
    supplier = Supplier(**data.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def get_suppliers(db: Session, skip=0, limit=20):
    return db.query(Supplier).offset(skip).limit(limit).all()

def get_supplier(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def update_supplier(db: Session, supplier_id: int, data: SupplierUpdate):
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return None
    for field, value in data.model_dump().items():
        setattr(supplier, field, value)
    db.commit()
    db.refresh(supplier)
    return supplier

def delete_supplier(db: Session, supplier_id: int):
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return None
    db.delete(supplier)
    db.commit()
    return supplier
