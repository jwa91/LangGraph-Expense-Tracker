import base64

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")

    return encoded_image

def image_encoder_node(state):

    new_state = state.copy()  

    image_location = state.get("image_location", "").strip()
    image_base64 = encode_image(image_location)

    new_state["image_base64"] = image_base64

    return new_state
