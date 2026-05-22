from locust import HttpUser, task, between
from bs4 import BeautifulSoup

class BookStackUser(HttpUser):
    wait_time = between(1, 3)  # attente entre chaque action

    def on_start(self):
        response = self.client.get("/login")
        soup = BeautifulSoup(response.text, "html.parser")
        token = soup.find("input", {"name": "_token"})["value"]
        # appelé une fois au démarrage de chaque utilisateur
        self.client.post("/login", {
            "email": "admin@admin.com",
            "password": "password",
            "_token": token
        })

    @task
    def read_page(self):
        self.client.get("/")  # page d'accueil  # quelle URL pour lire une page ?