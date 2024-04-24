import yaml
import requests

BASE_URL = "http://localhost:8000"
CATEGORIES_ENDPOINT = f"{BASE_URL}/categories"
PAYMENT_METHODS_ENDPOINT = f"{BASE_URL}/payment_methods"

config_path = "config.yaml"
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

categories = config.get("categories", [])
payment_methods = config.get("payment_methods", [])

def send_post_request(endpoint, data):
    response = requests.post(endpoint, json=data)
    if response.status_code in (200, 201):
        print(f"Successfully created: {data}")
    else:
        print(f"Error creating {data}: {response.status_code}")
    return response

for category in categories:
    category_data = {"category_name": category}
    send_post_request(CATEGORIES_ENDPOINT, category_data)

for payment_method in payment_methods:
    payment_method_data = {"payment_method_name": payment_method}
    send_post_request(PAYMENT_METHODS_ENDPOINT, payment_method_data)
