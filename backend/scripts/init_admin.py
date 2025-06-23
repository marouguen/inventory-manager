import os
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from dotenv import load_dotenv

load_dotenv()

def create_default_admin(db: Session):
    email = os.getenv("DEFAULT_ADMIN_EMAIL", "m.a.marouguen@gmail.com")
    password = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")

    existing = db.query(User).filter(User.email == email).first()
    if not existing:
        print(f"🔐 Creating admin user: {email}")
        new_user = User(
            email=email,
            hashed_password=get_password_hash(password),
            is_active=True,
            role="admin",
        )
        db.add(new_user)
        db.commit()
        print("✅ Admin created")
    else:
        print(f"👤 Admin already exists: {email}")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        create_default_admin(db)
    finally:
        db.close()
