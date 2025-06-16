from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

def create_category(db: Session, data: CategoryCreate):
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session, skip=0, limit=20):
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def update_category(db: Session, category_id: int, data: CategoryUpdate):
    category = get_category(db, category_id)
    if not category:
        return None
    for field, value in data.model_dump().items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    if not category:
        return None
    db.delete(category)
    db.commit()
    return category
