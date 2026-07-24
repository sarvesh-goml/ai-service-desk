from tests.conftest import client

def test_update_ticket_missing_ticket_id_param():
    payload = {
        "title": "Updated Title"
    }
    response = client.put("/tickets/update", json=payload)
    assert response.status_code == 422

def test_update_ticket_invalid_priority_enum():
    payload = {
        "priority": "dfsdfsdfsdf"
    }
    response = client.put("/tickets/update?ticket_id=123e4567-e89b-12d3-a456-426614174000", json=payload)
    assert response.status_code == 422

def test_update_ticket_not_found():
    payload = {
        "title": "Updated Title",
        "description": "Updated Description",
        "priority": "high",
        "isOpen": False
    }
    response = client.put("/tickets/update?ticket_id=123e4567-e89b-12d3-a456-426614174000", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 404
    assert data["message"] == "Ticket not found"

def test_update_ticket_invalid_is_open_type():
    payload = {
        "isOpen": "dfsdfsddfsfd"
    }
    response = client.put("/tickets/update?ticket_id=123e4567-e89b-12d3-a456-426614174000", json=payload)
    assert response.status_code == 422


