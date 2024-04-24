import yaml
import requests

# API-endpoints
BASE_URL = "http://localhost:8000"
CATEGORIES_ENDPOINT = f"{BASE_URL}/categories"
PAYMENT_METHODS_ENDPOINT = f"{BASE_URL}/payment_methods"

# Laad de configuratie vanuit de YAML-file
config_path = "config.yaml"
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

# Verkrijg de categorieën en betaalmethoden uit de configuratie
categories = config.get("categories", [])
payment_methods = config.get("payment_methods", [])

# Functie om POST-verzoeken te verzenden en resultaten te verwerken
def send_post_request(endpoint, data):
    response = requests.post(endpoint, json=data)
    if response.status_code in (200, 201):
        print(f"Successfully created: {data}")
    else:
        print(f"Error creating {data}: {response.status_code}")
    return response

# Voeg categorieën toe via POST-verzoeken
for category in categories:
    category_data = {"category_name": category}
    send_post_request(CATEGORIES_ENDPOINT, category_data)

# Voeg betaalmethoden toe via POST-verzoeken
for payment_method in payment_methods:
    payment_method_data = {"payment_method_name": payment_method}
    send_post_request(PAYMENT_METHODS_ENDPOINT, payment_method_data)
