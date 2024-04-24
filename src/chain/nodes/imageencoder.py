import base64

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")

    return encoded_image

def image_encoder_node(state):
    # Log when de node wordt aangeroepen
    print("image_encoder_node called with state:", state)

    # Haal de huidige waarden op
    new_state = state.copy()  # Maak een kopie van de bestaande state

    # Verkrijg de image locatie en encodeer deze
    image_location = state.get("image_location", "").strip()
    image_base64 = encode_image(image_location)

    # Voeg de nieuwe waarde toe aan de gekopieerde state
    new_state["image_base64"] = image_base64

    # Log wat de node retourneert
    print("image_encoder_node returning:", new_state)

    # Retourneer de bijgewerkte state
    return new_state
