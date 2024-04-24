from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing import Dict

# Definieer een data-model voor de categorizer
class CategoryData(BaseModel):
    category: str = Field(default=None, description="The selected category for the invoice")

# Functie om de lijst met categorieën uit de state te halen
def get_category_list(state):
    categories_dict = state.get("categories_dict", {})
    return list(categories_dict.values())

def categorize_invoice(state):
    # Extract de relevante velden uit de state
    receipt_date = state.get("date", None)
    receipt_description = state.get("description", None)
    receipt_amount = state.get("amount", None)
    receipt_vat = state.get("vat", None)
    receipt_business_personal = state.get("business_personal", None)
    receipt_payment_method = state.get("payment_method", None)

    category_list = get_category_list(state)

    # Stel de prompt voor de LLM op
    prompt = (
        f"Here's the summary of an invoice: \n"
        f"Date: {receipt_date}\n"
        f"Description: {receipt_description}\n"
        f"Amount: {receipt_amount}\n"
        f"VAT: {receipt_vat}\n"
        f"Business or Personal: {receipt_business_personal}\n"
        f"Payment Method: {receipt_payment_method}\n\n"
        f"Select an appropriate category for this invoice from the following list:\n"
        f"{', '.join(category_list)}"
    )

    # Kies het model op basis van de state
    categorizer_model_name = state.get("categorizer_model_name", "gpt-3.5-turbo")

    if "claude" in categorizer_model_name.lower():
        chat = ChatAnthropic(model=categorizer_model_name, temperature=0)
    else:
        chat = ChatOpenAI(model=categorizer_model_name, temperature=0)

    # Stel de gestructureerde LLM in met het CategoryData-schema
    structured_llm = chat.with_structured_output(CategoryData)

    # Stel het bericht op voor de LLM
    messages = [HumanMessage(content=[{"type": "text", "text": prompt}])]

    # Krijg de categorie van de LLM
    response = structured_llm.invoke(messages)

    # Haal de geselecteerde categorie op uit de LLM-respons
    selected_category = response.dict().get("category", None)

    # Maak een kopie van de bestaande state en werk deze bij
    new_state = state.copy()

    # Voeg de nieuwe of bijgewerkte waarden toe aan de gekopieerde state
    new_state["category"] = selected_category

    # Voeg de category_id toe op basis van categories_dict
    if 'category' in new_state and 'categories_dict' in new_state:
        category = new_state["category"]
        categories_dict = new_state["categories_dict"]
        for key, value in categories_dict.items():
            if value == category:
                new_state["category_id"] = key
                break

    # Voeg de payment_method_id toe op basis van payment_methods_dict
    if 'payment_method' in new_state and 'payment_methods_dict' in new_state:
        payment_method = new_state["payment_method"]
        payment_methods_dict = new_state["payment_methods_dict"]
        for key, value in payment_methods_dict.items():
            if value == payment_method:
                new_state["payment_method_id"] = key
                break

    return new_state

# Node-functie die de state bijwerkt
def categorizer_node(state):
    print("categorizer_node called with state:", state)

    # Update de state met categorize_invoice
    updated_state = categorize_invoice(state)

    print("categorizer_node returning:", updated_state)

    return updated_state
