from tests.conftest import client

def test_get_all_tickets():
    response = client.get("/tickets/get_tickets")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200

def test_get_tickets_filter_by_priority():
    response = client.get("/tickets/get_tickets?priority=high")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200

def test_get_tickets_filter_by_is_open():
    response = client.get("/tickets/get_tickets?isOpen=true")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200

def test_get_tickets_filter_by_priority_and_is_open():
    response = client.get("/tickets/get_tickets?priority=low&isOpen=false")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200

def test_get_ticket_by_id_not_found():
    response = client.get("/tickets/get_tickets?ticket_id=123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 404
    assert data["message"] == "Ticket not found"
    assert data["ticket"] is None

def test_get_tickets_invalid_is_open_param():
    response = client.get("/tickets/get_tickets?isOpen=dfsdfsdfg")
    assert response.status_code == 422

def test_get_tickets_invalid_uuid():
    response = client.get("/tickets/get_tickets?ticket_id=233455")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 404
