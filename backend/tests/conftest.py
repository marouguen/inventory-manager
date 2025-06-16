
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from fastapi.testclient import TestClient
from app.core.security import get_password_hash
from app.models import User, Category, Supplier


# Define the test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create DB fixture
@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db(db_engine):
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# ⛔️ IMPORTANT: Override BEFORE app is imported!
@pytest.fixture()
def client(db):
    from app import deps  # Import deps early to patch get_db
    

    def override_get_db():
        yield db

    from fastapi.testclient import TestClient
    from app.main import app  # Import app AFTER patching deps
    
    app.dependency_overrides[deps.get_db] = override_get_db

    app.dependency_overrides[deps.get_current_user] = lambda: db.query(User).filter_by(email="admin@example.com").first()
    
    with TestClient(app) as c:
        yield c

    

@pytest.fixture
def create_test_users(db):
    from app.models import User

    admin = db.query(User).filter_by(email="admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("adminpass"),
            is_active=True,
            role="admin"
        )
        db.add(admin)

    staff = db.query(User).filter_by(email="staff@example.com").first()
    if not staff:
        staff = User(
            email="staff@example.com",
            hashed_password=get_password_hash("staffpass"),
            is_active=True,
            role="staff"
        )
        db.add(staff)

    db.commit()
    db.refresh(admin)
    db.refresh(staff)

    return admin, staff



@pytest.fixture
def admin_token(client, create_test_users):
    response = client.post(
        "/login",
        data={"username": "admin@example.com", "password": "adminpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def staff_token(client, create_test_users):
    response = client.post(
        "/login",
        data={"username": "staff@example.com", "password": "staffpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def create_category_and_supplier(db):
    # Create a category if not exists
    category = db.query(Category).filter_by(name="Default Category").first()
    if not category:
        category = Category(name="Default Category")
        db.add(category)

    # Create a supplier if not exists
    supplier = db.query(Supplier).filter_by(name="Default Supplier").first()
    if not supplier:
        supplier = Supplier(
            name="Default Supplier",
            email="default@supplier.com",
            phone="123456789"
        )
        db.add(supplier)

    db.commit()
    db.refresh(category)
    db.refresh(supplier)

    return category.id, supplier.id
