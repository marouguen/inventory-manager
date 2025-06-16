import uuid

from app.models import User
from app.core.security import get_password_hash

def ensure_admin_user(db):
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
    # return admin
    pass

def create_product(client, token, category_id, supplier_id):
    # unique_suffix = str(uuid.uuid4())[:8]
    # response = client.post(
    #     "/products/",
    #     json={
    #         "name": f"Stock Test Product {unique_suffix}",
    #         "sku": f"STOCKSKU-{unique_suffix}",
    #         "barcode": f"1234567890{unique_suffix}",
    #         "quantity": 0,
    #         "unit": "pcs",
    #         "category_id": category_id,
    #         "supplier_id": supplier_id
    #     },
    #     headers={"Authorization": f"Bearer {token}"}
    # )
    # return response.json()["id"]
    pass

def test_create_stock(client, admin_token, db, create_category_and_supplier):
    # # Force re-create the admin user in the same DB session to ensure FK works
    # from app.models import User
    # from app.core.security import get_password_hash

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

    # category_id, supplier_id = create_category_and_supplier

    # # Create a product
    # product_id = create_product(client, admin_token, category_id, supplier_id)

    # # Create stock movement
    # response = client.post(
    #     "/stock/in",
    #     json={
    #         "product_id": product_id,
    #         "quantity": 50,
    #         "type": "in"
    #     },
    #     headers={"Authorization": f"Bearer {admin_token}"}
    # )

    # assert response.status_code in [200, 201]
    pass



# def test_update_stock(client, admin_token, create_category_and_supplier):
#     category_id, supplier_id = create_category_and_supplier
#     product_id = create_product(client, admin_token, category_id, supplier_id)

#     # Create first
#     create_response = client.post(
#         "/stocks/",
#         json={"product_id": product_id, "quantity": 30, "location": "Main"},
#         headers={"Authorization": f"Bearer {admin_token}"}
#     )
#     stock_id = create_response.json()["id"]

#     # Update
#     response = client.put(
#         f"/stocks/{stock_id}",
#         json={"product_id": product_id, "quantity": 60, "location": "Main Updated"},
#         headers={"Authorization": f"Bearer {admin_token}"}
#     )

#     assert response.status_code == 200
#     data = response.json()
#     assert data["quantity"] == 60
#     assert data["location"] == "Main Updated"


# def test_get_stock_by_id(client, admin_token, create_category_and_supplier):
#     category_id, supplier_id = create_category_and_supplier
#     product_id = create_product(client, admin_token, category_id, supplier_id)

#     create_response = client.post(
#         "/stocks/",
#         json={"product_id": product_id, "quantity": 20, "location": "Rack 1"},
#         headers={"Authorization": f"Bearer {admin_token}"}
#     )
#     stock_id = create_response.json()["id"]

#     response = client.get(f"/stocks/{stock_id}")
#     assert response.status_code == 200
#     assert response.json()["id"] == stock_id


# def test_delete_stock(client, admin_token, create_category_and_supplier):
#     category_id, supplier_id = create_category_and_supplier
#     product_id = create_product(client, admin_token, category_id, supplier_id)

#     create_response = client.post(
#         "/stocks/",
#         json={"product_id": product_id, "quantity": 10, "location": "Temp"},
#         headers={"Authorization": f"Bearer {admin_token}"}
#     )
#     stock_id = create_response.json()["id"]

#     response = client.delete(
#         f"/stocks/{stock_id}",
#         headers={"Authorization": f"Bearer {admin_token}"}
#     )

#     assert response.status_code == 204
