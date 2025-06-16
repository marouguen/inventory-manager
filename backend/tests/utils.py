import uuid

def create_product(client, token, category_id, supplier_id):
    unique_suffix = str(uuid.uuid4())[:8]
    response = client.post(
        "/products/",
        json={
            "name": f"Product {unique_suffix}",
            "sku": f"SKU-{unique_suffix}",
            "barcode": f"BAR{unique_suffix}",
            "quantity": 0,
            "unit": "pcs",
            "category_id": category_id,
            "supplier_id": supplier_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()["id"]
