import requests

def db_entry_node(state):
    # Extracting values from the given state
    date = state.get("date", "").strip()
    category_id = state.get("category_id", "").strip()
    description = state.get("description", "").strip()
    amount = state.get("amount", "").strip()
    vat = state.get("vat", "").strip()
    business_personal = state.get("business_personal", "").strip()
    payment_method_id = state.get("payment_method_id", "").strip()

    # The endpoint URL
    url = "http://localhost:8000/expenses"
    
    # Data to be sent in the POST request
    data = {
        "date": date,
        "category_id": category_id,
        "description": description,
        "amount": amount,
        "vat": vat,
        "payment_method_id": payment_method_id,
        "business_personal": business_personal
    }
    
    # Make the POST request to the endpoint
    try:
        response = requests.post(url, json=data)
        
        # Check if the request was successful
        if response.status_code == 201:
            print("Expense created successfully.")
        else:
            print("Failed to create expense.")
            print("Status Code:", response.status_code)
            print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error while making the API request:", e)
