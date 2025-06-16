from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierOut
from app.crud import supplier as crud
from app.db.database import SessionLocal
from app.deps import get_current_user, require_admin

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SupplierOut, status_code=201)
def create(data: SupplierCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return crud.create_supplier(db, data)

@router.get("/", response_model=List[SupplierOut])
def list(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_suppliers(db, skip, limit)

@router.get("/{supplier_id}", response_model=SupplierOut)
def get(supplier_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    supplier = crud.get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.put("/{supplier_id}", response_model=SupplierOut)
def update(supplier_id: int, data: SupplierUpdate, db: Session = Depends(get_db), user=Depends(require_admin)):
    supplier = crud.update_supplier(db, supplier_id, data)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.delete("/{supplier_id}")
def delete(supplier_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    supplier = crud.delete_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"detail": f"Deleted supplier {supplier.name}"}
