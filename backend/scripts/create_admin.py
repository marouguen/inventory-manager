import sys
import os
from getpass import getpass

# Setup Django-like path handling
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def main():
    db: Session = SessionLocal()

    email = input("Admin email: ").strip()
    password = getpass("Admin password: ").strip()

    if db.query(User).filter(User.email == email).first():
        print("❌ A user with this email already exists.")
        return

    hashed_password = get_password_hash(password)

    admin = User(
        email=email,
        hashed_password=hashed_password,
        role="admin",
        is_active=True,
        profile_pic=None
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print(f"✅ Admin user created: {admin.email} (id={admin.id})")

if __name__ == "__main__":
    main()
