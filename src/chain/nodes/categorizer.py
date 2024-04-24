from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class CategoryData(BaseModel):
    category: str = Field(default=None, description="The selected category for the invoice")

def get_category_list(state):
    categories_dict = state.get("categories_dict", {})
    return list(categories_dict.values())

def categorize_invoice(state):
    receipt_date = state.get("date", None)
    receipt_description = state.get("description", None)
    receipt_amount = state.get("amount", None)
    receipt_vat = state.get("vat", None)
    receipt_business_personal = state.get("business_personal", None)
    receipt_payment_method = state.get("payment_method", None)

    category_list = get_category_list(state)

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

    categorizer_model_name = state.get("categorizer_model_name", "gpt-3.5-turbo")

    if "claude" in categorizer_model_name.lower():
        chat = ChatAnthropic(model=categorizer_model_name, temperature=0)
    else:
        chat = ChatOpenAI(model=categorizer_model_name, temperature=0)

    structured_llm = chat.with_structured_output(CategoryData)

    messages = [HumanMessage(content=[{"type": "text", "text": prompt}])]

    response = structured_llm.invoke(messages)

    selected_category = response.dict().get("category", None)

    new_state = state.copy()

    new_state["category"] = selected_category

    if 'category' in new_state and 'categories_dict' in new_state:
        category = new_state["category"]
        categories_dict = new_state["categories_dict"]
        for key, value in categories_dict.items():
            if value == category:
                new_state["category_id"] = key
                break

    if 'payment_method' in new_state and 'payment_methods_dict' in new_state:
        payment_method = new_state["payment_method"]
        payment_methods_dict = new_state["payment_methods_dict"]
        for key, value in payment_methods_dict.items():
            if value == payment_method:
                new_state["payment_method_id"] = key
                break

    return new_state

def categorizer_node(state):

    updated_state = categorize_invoice(state)

    return updated_state
