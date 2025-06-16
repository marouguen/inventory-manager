# tests/test_auth.py
from app.models import User
from app.db.database import SessionLocal
from app.models import User
from app.db.database import SessionLocal
from app.core.security import get_password_hash

def test_register_user(client):
    # Ensure test user does not exist
    db = SessionLocal()
    db.query(User).filter_by(email="testuser@example.com").delete()
    db.commit()
    db.close()

    response = client.post("/register", json={
        "email": "testuser@example.com",
        "password": "strongpassword"
    })

    print("First Register Response:", response.status_code, response.json())
    assert response.status_code == 200



def test_login_user(client):
    db = SessionLocal()
    
    # Make sure the user exists in DB
    hashed = get_password_hash("strongpassword")
    user = User(email="testuser@example.com", hashed_password=hashed, is_active=True)
    db.query(User).filter_by(email="testuser@example.com").delete()
    db.add(user)
    db.commit()
    db.close()

    # OAuth2PasswordRequestForm requires form-encoded data
    response = client.post(
        "/login",
        data={
            "username": "testuser@example.com",
            "password": "strongpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    print("Login Response:", response.status_code, response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_invalid_login(client):
    # Wrong password
    response = client.post(
        "/login",
        data={
            "username": "testuser@example.com",
            "password": "wrongpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    print("Invalid Login Response:", response.status_code, response.json())
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_inactive_user(client, db):
    # Manually create an inactive user
    from app.models import User
    from app.core.security import get_password_hash

    inactive_email = "inactive@example.com"        
    user = User(
        email=inactive_email,
        hashed_password=get_password_hash("inactivepass"),
        is_active=False,
        role="staff"
    )
    db.add(user)
    db.commit()

    # Try to log in
    response = client.post(
        "/login",
        data={
            "username": inactive_email,
            "password": "inactivepass"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    print("Inactive User Login Response:", response.status_code, response.json())
    assert response.status_code == 401