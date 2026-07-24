from tests.conftest import client

def test_delete_ticket_missing_ticket_id_param():
    response = client.delete("/tickets/delete")
    assert response.status_code == 422

def test_delete_ticket_not_found():
    response = client.delete("/tickets/delete?ticket_id=123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 404
    assert data["message"] == "Ticket not found"

def test_delete_ticket_invalid_id_format():
    response = client.delete("/tickets/delete?ticket_id=12345")
    assert response.status_code == 422
