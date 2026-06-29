def test_register_success(client):
    resp = client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_register_duplicate_username(client):
    payload = {"username": "bob", "email": "bob@example.com", "password": "pw"}
    client.post("/auth/register", json=payload)
    resp = client.post("/auth/register", json={**payload, "email": "other@example.com"})
    assert resp.status_code == 400
    assert "Username" in resp.json()["detail"]


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "username": "carol", "email": "carol@example.com", "password": "pw"
    })
    resp = client.post("/auth/register", json={
        "username": "carol2", "email": "carol@example.com", "password": "pw"
    })
    assert resp.status_code == 400
    assert "Email" in resp.json()["detail"]


def test_login_success(client, registered_user):
    resp = client.post("/auth/login", json={"username": "testuser", "password": "secret123"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "testuser"


def test_login_wrong_password(client, registered_user):
    resp = client.post("/auth/login", json={"username": "testuser", "password": "wrong"})
    assert resp.status_code == 401


def test_login_unknown_user(client):
    resp = client.post("/auth/login", json={"username": "nobody", "password": "pw"})
    assert resp.status_code == 401


def test_logout(client, auth_headers):
    resp = client.post("/auth/logout", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Logged out successfully"


def test_logout_requires_auth(client):
    resp = client.post("/auth/logout")
    assert resp.status_code == 401
