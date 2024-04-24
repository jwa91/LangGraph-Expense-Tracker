
def correct_node(state):
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

    # Vraag de gebruiker om instructies voor aanpassingen
    instructions = input("Let the model know what you want it to change, for example: change the expense type to business: ")

    # Sla de gebruikerkeuze op in de state voor verdere verwerking
    state["user_instructions"] = instructions  # sla de invoer op in de state