from locust import HttpUser, between, task
 
 
class TicketApiUser(HttpUser):
    wait_time = between(1, 3)
 
    @task(3)
    def check_health(self) -> None:
        self.client.get("/health", name="GET /health")
 
    @task(2)
    def list_tickets(self) -> None:
        self.client.get("/tickets", name="GET /tickets")
 
    @task(1)
    def create_ticket(self) -> None:
        self.client.post(
            "/tickets",
            name="POST /tickets",
            json={
                "title": "Load test ticket",
                "description": "A realistic ticket created by a simulated user.",
                "severity": 3,
                "customer_type": "premium",
            },
        )