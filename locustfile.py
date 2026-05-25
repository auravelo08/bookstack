from locust import HttpUser, task, between
from bs4 import BeautifulSoup

class BookStackUser(HttpUser): # Simule un utilisateur BookStack
    wait_time = between(1, 3)  # attente entre chaque action

    def on_start(self):                                       # Appelé une fois au démarrage de chaque utilisateur simulé
        response = self.client.get("/login")                  # Charge la page de login (GET)
        soup = BeautifulSoup(response.text, "html.parser")    # Parse le HTML reçu avec BeautifulSoup
        token_input = soup.find("input", {"name": "_token"})  # Cherche le champ caché _token (CSRF) dans le HTML
        if token_input:                                       # Vérifie que le token existe (évite un crash si erreur 500)
            self.client.post("/login", {                      # Soumet le formulaire de login (POST)
                "email": "admin@admin.com",
                "password": "password",
                "_token": token_input["value"]                # Renvoie le token CSRF à Laravel pour validation
            })

    @task
    def read_page(self):
        self.client.get("/shelves")  # page qui amènes aux étagères