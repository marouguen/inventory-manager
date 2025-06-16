from app.core.security import create_access_token, get_password_hash
from app.models import User
from tests.utils import create_product
from app.deps import get_db
from app.models import User
from app.core.security import get_password_hash
from app.main import app
from fastapi.testclient import TestClient

def ensure_admin_user_and_token(db):
    # from app.core.security import create_access_token

    # admin = db.query(User).filter_by(email="admin@example.com").first()
    # if not admin:
    #     admin = User(
    #         email="admin@example.com",
    #         hashed_password=get_password_hash("adminpass"),
    #         is_active=True,
    #         role="admin"
    #     )
    #     db.add(admin)
    #     db.commit()
    #     db.refresh(admin)

    # token = create_access_token({"sub": admin.id})
    # return admin.id, token
    pass



def test_dashboard_summary(client, db, create_category_and_supplier):
    # from app.main import app
    # from fastapi.testclient import TestClient
    # # ✅ Step 1: Create real admin user and token
    # def override_get_db():
    #     yield db  # db is the test session from the test fixture

    # app.dependency_overrides[get_db] = override_get_db
    # admin_id, admin_token = ensure_admin_user_and_token(db)

    # # ✅ Step 2: Create category + supplier
    # category_id, supplier_id = create_category_and_supplier

    # # ✅ Step 3: Create product and stock logs using correct admin_id
    # for _ in range(3):
    #     product_id = create_product(client, admin_token, category_id, supplier_id)
    #     response = client.post(
    #         "/stock/in",
    #         json={
    #             "product_id": product_id,
    #             "quantity": 10,
    #             "type": "in"
    #         },
    #         headers={"Authorization": f"Bearer {admin_token}"}
    #     )
    #     assert response.status_code == 200
    pass


