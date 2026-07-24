from tests.conftest import client



def test_ticket_lifecycle_end_to_end():
    payload = {
        "title": "End to end ticket",
        "description": "Full ticket lifecycle test",
        "priority": "low",
        "isOpen": True,
        "email": "user@example.com"
    }

    create_response = client.post("/tickets", json=payload)
    assert create_response.status_code == 200
    ticket_id = create_response.json()["ticket_id"]

    try:
        get_response = client.get(f"/tickets/{ticket_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == payload["title"]

        update_response = client.put(
            f"/tickets/{ticket_id}",
            json={
                "title": "End to end ticket updated",
                "isOpen": False
            }
        )
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "closed"

        delete_response = client.delete(f"/tickets/{ticket_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["ticket_id"] == ticket_id

        missing_response = client.get(f"/tickets/{ticket_id}")
        assert missing_response.status_code == 404
    finally:
        client.delete(f"/tickets/{ticket_id}")
