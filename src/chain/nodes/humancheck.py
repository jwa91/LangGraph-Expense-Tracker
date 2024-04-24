def humancheck_node(state):
    image_location = state.get("image_location", "").strip()
    date = state.get("date", "").strip()
    category = state.get("category", "").strip()
    description = state.get("description", "").strip()
    amount = state.get("amount", "").strip()
    vat = state.get("vat", "").strip()
    business_personal = state.get("business_personal", "").strip()
    payment_method = state.get("payment_method", "").strip()

    print(f"Image location: {image_location}")
    print(f"Date: {date}")
    print(f"Category: {category}")
    print(f"Description: {description}")
    print(f"Amount: {amount}")
    print(f"Vat: {vat}")
    print(f"Business or Personal: {business_personal}")
    print(f"Payment method: {payment_method}")

    choice = input("Accept(a), Change Model (m) or Correct (c)? ")

    new_state = state.copy()

    if choice.lower() == 'a':
        new_state["user_decision"] = "accept"
    elif choice.lower() == 'm':
        new_state["user_decision"] = "change_model"

        if new_state["vision_model_name"] == "gpt-4-vision-preview":
            new_state["vision_model_name"] = "claude-3-opus-20240229"
        else:
            new_state["vision_model_name"] = "gpt-4-vision-preview"

        if new_state["categorizer_model_name"] == "gpt-4-turbo":
            new_state["categorizer_model_name"] = "claude-3-sonnet-20240229"
        else:
            new_state["categorizer_model_name"] = "gpt-4-turbo"

    elif choice.lower() == 'c':
        new_state["user_decision"] = "correct"

    return new_state
