import requests

def get_payment_methods() -> dict:
    url = 'http://localhost:8000/payment_methods'
    response = requests.get(url, headers={"accept": "application/json"})

    if response.status_code == 200:
        payment_methods = response.json()
        # Create a dictionary with ID as the key and payment method name as the value
        payment_methods_dict = {
            item["payment_method_id"]: item["payment_method_name"]
            for item in payment_methods
        }
        return payment_methods_dict
    else:
        raise Exception("Failed to fetch payment methods. Status code: {}".format(response.status_code))


def get_categories() -> dict:
    url = 'http://localhost:8000/categories'
    response = requests.get(url, headers={"accept": "application/json"})

    if response.status_code == 200:
        categories = response.json()
        # Create a dictionary with ID as the key and category name as the value
        categories_dict = {
            item["category_id"]: item["category_name"]
            for item in categories
        }
        return categories_dict
    else:
        raise Exception("Failed to fetch categories. Status code: {}".format(response.status_code))
