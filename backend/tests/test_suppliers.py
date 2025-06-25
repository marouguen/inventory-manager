import uuid

def test_create_supplier(client, admin_token):
    unique_name = f"Test Supplier {uuid.uuid4().hex[:6]}"
    response = client.post(
        "/api/suppliers/",
        json={
            "name": unique_name,
            "email": f"{unique_name.lower()}@example.com",
            "phone": "123-456-7890"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 201
#################################################

def test_get_all_suppliers(client, admin_token):
    response = client.get(
        "/api/suppliers/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    if data:  # Optional: Check structure of the first item if list is not empty
        supplier = data[0]
        assert "id" in supplier
        assert "name" in supplier
        assert "email" in supplier
        assert "phone" in supplier
#####################################################

from uuid import uuid4

def test_get_supplier_by_id(client, admin_token):
    unique_name = f"Supplier-{uuid4()}"

    # Create a new supplier with a unique name
    create_response = client.post(
        "/api/suppliers/",
        json={
            "name": unique_name,
            "email": "one@supplier.com",
            "phone": "111-222-3333"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_response.status_code in [200, 201]

    supplier_id = create_response.json()["id"]

    # Get the supplier by ID
    get_response = client.get(
        f"/api/suppliers/{supplier_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_response.status_code == 200
    assert get_response.json()["name"] == unique_name



############################################################

def test_delete_supplier(client, admin_token):
    # Create a supplier first
    create_response = client.post(
        "/api/suppliers/",
        json={
            "name": "Delete Me Inc.",
            "email": "delete@me.com",
            "phone": "555-555-5555"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_response.status_code in [200, 201]
    supplier_id = create_response.json()["id"]

    # Delete the supplier
    delete_response = client.delete(f"/api/suppliers/{supplier_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Deleted supplier Delete Me Inc."


    # Confirm it's gone
    get_response = client.get(f"/api/suppliers/{supplier_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert get_response.status_code == 404

####################################################

import uuid

def test_update_supplier(client, admin_token):
    unique_suffix = str(uuid.uuid4())[:8]  # Short unique ID

    # Step 1: Create a supplier to update
    create_response = client.post(
        "/api/suppliers/",
        json={
            "name": f"Original Supplier {unique_suffix}",
            "email": f"original{unique_suffix}@supplier.com",
            "phone": "999-999-9999"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_response.status_code in [200, 201]
    supplier_id = create_response.json()["id"]

    # Step 2: Update the supplier
    update_data = {
        "name": f"Updated Supplier {unique_suffix}",
        "email": f"updated{unique_suffix}@supplier.com",
        "phone": "888-888-8888",
        "address": "123 Updated Street"
    }
    update_response = client.put(
        f"/api/suppliers/{supplier_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert update_response.status_code == 200
    updated_supplier = update_response.json()

    # Step 3: Verify updates
    assert updated_supplier["name"] == update_data["name"]
    assert updated_supplier["email"] == update_data["email"]
    assert updated_supplier["phone"] == update_data["phone"]
    assert updated_supplier["address"] == update_data["address"]

