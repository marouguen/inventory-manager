from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.crud import category as crud
from app.db.database import SessionLocal
from app.deps import get_current_user, require_admin

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategoryOut, status_code=201)
def create(data: CategoryCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return crud.create_category(db, data)

@router.get("/", response_model=List[CategoryOut])
def list(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_categories(db, skip, limit)

@router.get("/{category_id}", response_model=CategoryOut)
def get(category_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryOut)
def update(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db), user=Depends(require_admin)):
    category = crud.update_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}")
def delete(category_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    category = crud.delete_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": f"Deleted category {category.name}"}
