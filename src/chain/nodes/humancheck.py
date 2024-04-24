def humancheck_node(state):
    # Log de huidige state
    print("humancheck_node called with state:", state)

    # Verkrijg belangrijke informatie uit de state
    image_location = state.get("image_location", "").strip()
    date = state.get("date", "")
    category = state.get("category", "")
    description = state.get("description", "")
    amount = state.get("amount", "")

    # Toon de informatie aan de gebruiker
    print(f"Afbeelding locatie: {image_location}")
    print(f"Datum: {date}")
    print(f"Categorie: {category}")
    print(f"Beschrijving: {description}")
    print(f"Bedrag: {amount}")

    # Vraag de gebruiker om een keuze
    choice = input("Wilt u deze informatie accepteren (a), het model wijzigen (m), of corrigeren (c)? ")

    # Maak een kopie van de state
    new_state = state.copy()

    # Afhankelijk van de keuze, pas de state aan
    if choice.lower() == 'a':
        new_state["user_decision"] = "accept"
    elif choice.lower() == 'm':
        new_state["user_decision"] = "change_model"

        # Update vision_model_name volgens de gegeven voorwaarden
        if new_state["vision_model_name"] == "gpt-4-vision-preview":
            new_state["vision_model_name"] = "claude-3-opus-20240229"
        else:
            new_state["vision_model_name"] = "gpt-4-vision-preview"

        # Update categorizer_model_name volgens de gegeven voorwaarden
        if new_state["categorizer_model_name"] == "gpt-4-turbo":
            new_state["categorizer_model_name"] = "claude-3-sonnet-20240229"
        else:
            new_state["categorizer_model_name"] = "gpt-4-turbo"

    elif choice.lower() == 'c':
        new_state["user_decision"] = "correct"

    # Log wat de node retourneert
    print("humancheck_node returning:", new_state)

    # Retourneer de aangepaste state
    return new_state
