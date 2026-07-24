from tests.conftest import client



def test_create_ticket_and_fetch_by_id():
    payload = {
        "title": "Integration ticket one",
        "description": "Create then fetch by id",
        "priority": "high",
        "isOpen": True,
        "email": "user@example.com"
    }

    create_response = client.post("/tickets", json=payload)
    assert create_response.status_code == 200
    ticket_id = create_response.json()["ticket_id"]

    try:
        fetch_response = client.get(f"/tickets/{ticket_id}")
        assert fetch_response.status_code == 200

        ticket = fetch_response.json()
        assert ticket["id"] == ticket_id
        assert ticket["title"] == payload["title"]
        assert ticket["priority"] == payload["priority"]
        assert ticket["status"] == "open"
    finally:
        client.delete(f"/tickets/{ticket_id}")



def test_create_ticket_and_update_it():
    payload = {
        "title": "Integration ticket two",
        "description": "Create then update",
        "priority": "medium",
        "isOpen": True,
        "email": "user@example.com"
    }

    create_response = client.post("/tickets", json=payload)
    assert create_response.status_code == 200
    ticket_id = create_response.json()["ticket_id"]

    try:
        update_payload = {
            "title": "Updated integration ticket",
            "description": "Updated description",
            "priority": "critical",
            "isOpen": False
        }

        update_response = client.put(f"/tickets/{ticket_id}", json=update_payload)
        assert update_response.status_code == 200

        ticket = update_response.json()
        assert ticket["id"] == ticket_id
        assert ticket["title"] == update_payload["title"]
        assert ticket["priority"] == update_payload["priority"]
        assert ticket["status"] == "closed"
    finally:
        client.delete(f"/tickets/{ticket_id}")
