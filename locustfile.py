from locust import HttpUser, task, between

class BookStackUser(HttpUser):
    wait_time = between(1, 3)  # attente entre chaque action

    def on_start(self):
        # appelé une fois au démarrage de chaque utilisateur
        self.client.post("/login", {
            "email": "admin@admin.com",
            "password": "password"
        })

    @task
    def read_page(self):
        self.client.get("/")  # page d'accueil  # quelle URL pour lire une page ?