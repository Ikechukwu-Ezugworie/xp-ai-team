def test_send_message(client, auth_headers):
    client.post("/rooms/", json={"name": "general"}, headers=auth_headers)
    rooms = client.get("/rooms/", headers=auth_headers).json()
    room_id = rooms[0]["id"]
    resp = client.post(f"/messages/{room_id}", json={"content": "Hello!"}, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["content"] == "Hello!"
    assert data["username"] == "testuser"
    assert "timestamp" in data


def test_get_message_history(client, auth_headers):
    client.post("/rooms/", json={"name": "history-room"}, headers=auth_headers)
    rooms = client.get("/rooms/", headers=auth_headers).json()
    room_id = next(r["id"] for r in rooms if r["name"] == "history-room")
    client.post(f"/messages/{room_id}", json={"content": "msg1"}, headers=auth_headers)
    client.post(f"/messages/{room_id}", json={"content": "msg2"}, headers=auth_headers)
    resp = client.get(f"/messages/{room_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_search_messages(client, auth_headers):
    client.post("/rooms/", json={"name": "search-room"}, headers=auth_headers)
    rooms = client.get("/rooms/", headers=auth_headers).json()
    room_id = next(r["id"] for r in rooms if r["name"] == "search-room")
    client.post(f"/messages/{room_id}", json={"content": "hello world"}, headers=auth_headers)
    client.post(f"/messages/{room_id}", json={"content": "goodbye"}, headers=auth_headers)
    resp = client.get(f"/messages/{room_id}/search?q=hello", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["messages"][0]["content"] == "hello world"


def test_message_unknown_room(client, auth_headers):
    resp = client.get("/messages/999", headers=auth_headers)
    assert resp.status_code == 404
