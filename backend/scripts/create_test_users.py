# scripts/create_test_users.py
import os 
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash



db = SessionLocal()

admin = db.query(User).filter(User.email == "admin@example.com").first()
if not admin:
    admin = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpass"),
        is_active=True,
        role="admin"
    )
    db.add(admin)

user = db.query(User).filter(User.email == "user@example.com").first()
if not user:
    user = User(
        email="user@example.com",
        hashed_password=get_password_hash("userpass"),
        is_active=True,
        role="staff"
    )
    db.add(user)

db.commit()
db.close()
print("✔ Test users created.")
