import sys
import os

# Make sure app is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Category, Supplier, Product, StockMovement

def load_data():
    db: Session = SessionLocal()

    # ✅ Path to JSON file relative to this script
    file_path = os.path.join(os.path.dirname(__file__), "dummy_inventory_data.json")

    with open(file_path, "r") as f:
        data = json.load(f)

    for cat in data["categories"]:
        db.add(Category(**cat))

    for supplier in data["suppliers"]:
        db.add(Supplier(**supplier))

    db.commit()

    for product in data["products"]:
        db.add(Product(**product))

    db.commit()

    for move in data["stock_movements"]:
        db.add(StockMovement(**move))

    db.commit()
    db.close()
    print("✅ Dummy data loaded successfully")

if __name__ == "__main__":
    load_data()
