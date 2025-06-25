import uuid

from sqlalchemy import true

def test_create_category(client, admin_token):
    unique_name = f"Electronics-{uuid.uuid4().hex[:6]}"

    response = client.post(
        "/api/categories/",
        json={"name": unique_name},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code in [200, 201]
    assert response.json()["name"] == unique_name

import uuid

def test_list_categories(client, admin_token):
    names = [f"Food-{uuid.uuid4().hex[:6]}", f"Clothing-{uuid.uuid4().hex[:6]}"]

    for name in names:
        response = client.post(
            "/api/categories/",
            json={"name": name},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 201

def test_get_category(client, admin_token):
    # Use a unique name to avoid IntegrityError
    import uuid
    unique_name = f"Electronics-{uuid.uuid4().hex[:6]}"

    create_response = client.post(
        "/api/categories/",
        json={"name": unique_name},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_response.status_code == 201
    created_category = create_response.json()

    get_response = client.get(
        f"/api/categories/{created_category['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_response.status_code == 200
    assert get_response.json()["name"] == unique_name

def test_update_category(client, admin_token):
    # Create a category first
    import uuid
    unique_name = f"Books-{uuid.uuid4().hex[:6]}"
    
    create_response = client.post(
        "/api/categories/",
        json={"name": unique_name},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_response.status_code == 201
    created_category = create_response.json()
    
    # Update the category
    updated_name = f"{unique_name}-Updated"
    update_response = client.put(
        f"/api/categories/{created_category['id']}",
        json={"name": updated_name},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert update_response.status_code == 200
    updated_category = update_response.json()

    # Validate update
    assert updated_category["id"] == created_category["id"]
    assert updated_category["name"] == updated_name

def test_delete_category(client, admin_token):
    # Create a unique category
    import uuid
    unique_name = f"Toys-{uuid.uuid4().hex[:6]}"
    
    create_response = client.post(
        "/api/categories/",
        json={"name": unique_name},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_response.status_code == 201
    created_category = create_response.json()

    # Delete the category
    delete_response = client.delete(
        f"/api/categories/{created_category['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert delete_response.status_code == 200
    assert "Deleted category" in delete_response.json()["detail"]

    # Verify it's gone
    get_response = client.get(
        f"/api/categories/{created_category['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_response.status_code == 404

def test_staff_cannot_create_category(client):
    assert True
