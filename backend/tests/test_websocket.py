from app.auth import create_access_token


def test_websocket_join_and_message(client, registered_user):
    auth_resp = client.post("/auth/login", json={"username": "testuser", "password": "secret123"})
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/rooms/", json={"name": "ws-room"}, headers=headers)
    rooms = client.get("/rooms/", headers=headers).json()
    room_id = rooms[0]["id"]

    with client.websocket_connect(f"/ws/{room_id}?token={token}") as ws:
        join_event = ws.receive_json()
        assert join_event["type"] == "join"
        assert join_event["username"] == "testuser"

        ws.send_json({"type": "message", "content": "Hello WS!"})
        msg_event = ws.receive_json()
        assert msg_event["type"] == "message"
        assert msg_event["content"] == "Hello WS!"
        assert msg_event["username"] == "testuser"


def test_websocket_typing_indicator(client, registered_user):
    token = create_access_token(registered_user["id"], registered_user["username"])
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/rooms/", json={"name": "typing-room"}, headers=headers)
    rooms = client.get("/rooms/", headers=headers).json()
    room_id = rooms[0]["id"]

    with client.websocket_connect(f"/ws/{room_id}?token={token}") as ws:
        ws.receive_json()  # join event
        ws.send_json({"type": "typing"})
        event = ws.receive_json()
        assert event["type"] == "typing"
        assert event["username"] == "testuser"
