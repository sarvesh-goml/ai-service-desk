from tests.conftest import client

def test_create_ticket():
    payload = {
        "title": "Bug in login", 
       "description": "User cannot log in",
        "priority": "high",
        "isOpen": True,
        "email": "user@example.com"
    }
    response = client.post("/tickets/", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == 201
    assert "ticket_id" in response.json()


def test_create_ticket_missing_title():
    payload = {
        "description": "Missing title",
        "email": "user@example.com"
    }
    response = client.post("/tickets/", json=payload)
    assert response.status_code == 422

def test_create_ticket_missing_description():
    payload = {
        "title": "Missing description",
        "email": "user@example.com"
    }
    response = client.post("/tickets/", json=payload)
    assert response.status_code == 422

def test_create_ticket_missing_email():
    payload = {
        "title": "Missing email",
        "description": "Some description"
    }
    response = client.post("/tickets/", json=payload)
    assert response.status_code == 422

def test_create_ticket_invalid_priority():
    payload = {
        "title": "Invalid Priority",
        "description": "Some issue",
        "priority": "invalid_priority",
        "email": "user@example.com"
    }
    response = client.post("/tickets/", json=payload)
    assert response.status_code == 422

def test_create_ticket_null_title():
    payload = {
        "title": None,
        "description": "Null title",
        "email": "user@example.com"
    }
    response = client.post("/tickets/", json=payload)
    assert response.status_code == 422

