import pytest

# ----------------------------
# CREATE PRODUCT
# ----------------------------
import uuid

def test_create_product(client, admin_token, create_category_and_supplier):
    category_id, supplier_id = create_category_and_supplier
    unique_suffix = uuid.uuid4().hex[:6]

    response = client.post(
        "/api/products/",
        json={
            "name": "Test Product",
            "sku": f"SKU-{unique_suffix}",
            "barcode": f"BAR-{unique_suffix}",
            "quantity": 100,
            "unit": "pcs",
            "category_id": category_id,
            "supplier_id": supplier_id
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code in [200, 201]
    data = response.json()
    assert data["name"] == "Test Product"



# ----------------------------
# GET PRODUCTS
# ----------------------------
def test_get_all_products(client):
    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# ----------------------------
# GET PRODUCT BY ID
# ----------------------------
import uuid

def test_get_product_by_id(client, admin_token, create_category_and_supplier):
    category_id, supplier_id = create_category_and_supplier
    unique = uuid.uuid4().hex[:6]

    create_response = client.post(
        "/api/products/",
        json={
            "name": "Unique Product",
            "sku": f"SKU-{unique}",
            "barcode": f"BAR-{unique}",
            "quantity": 5,
            "unit": "pcs",
            "category_id": category_id,
            "supplier_id": supplier_id
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    if create_response.status_code not in [200, 201]:
        pytest.skip("Failed to create product for retrieval test")

    product_id = create_response.json()["id"]

    response = client.get(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Unique Product"



# ----------------------------
# UPDATE PRODUCT
# ----------------------------
import uuid

def test_update_product(client, admin_token, create_category_and_supplier):
    category_id, supplier_id = create_category_and_supplier
    unique = uuid.uuid4().hex[:6]

    create_response = client.post(
        "/api/products/",
        json={
            "name": "Old Product",
            "sku": f"SKU-{unique}",
            "barcode": f"BAR-{unique}",
            "quantity": 50,
            "unit": "pcs",
            "category_id": category_id,
            "supplier_id": supplier_id
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert create_response.status_code in [200, 201], create_response.text
    product_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/products/{product_id}",
        json={
            "name": "Updated Product",
            "sku": f"SKU-{unique}-updated",
            "barcode": f"BAR-{unique}-updated",
            "quantity": 75,
            "unit": "pcs",
            "category_id": category_id,
            "supplier_id": supplier_id
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["name"] == "Updated Product"
    assert updated["quantity"] == 75

# ----------------------------
# DELETE PRODUCT
# ----------------------------
import uuid

def test_delete_product(client, admin_token, create_category_and_supplier):
    category_id, supplier_id = create_category_and_supplier
    unique = uuid.uuid4().hex[:6]

    # Create a product to delete
    create_response = client.post(
        "/api/products/",
        json={
            "name": "Delete Product",
            "sku": f"SKU-{unique}",
            "barcode": f"BAR-{unique}",
            "quantity": 20,
            "unit": "pcs",
            "category_id": category_id,
            "supplier_id": supplier_id
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert create_response.status_code in [200, 201], create_response.text
    product_id = create_response.json()["id"]

    # Delete the product
    delete_response = client.delete(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert delete_response.status_code == 200

    # Confirm deletion
    get_response = client.get(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_response.status_code == 404
