from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

class ReceiptData(BaseModel):
    date: str = Field(default=None, description="The date of the receipt")
    description: str = Field(default=None, description="A brief description of the payment")
    amount: str = Field(default=None, description="The total amount paid")
    vat: str = Field(default=None, description="The total VAT (taxes) paid")
    business_personal: str = Field(default=None, description="Indicate whether the payment is business or personal")
    payment_method: str = Field(default=None, description="Indicate the payment method")

def get_payment_methods(state):
    payment_methods_dict = state.get("payment_methods_dict", {})
    return list(payment_methods_dict.values())

def get_receipt_json(image_base64: str, state: dict):
    vision_model_name = state.get("vision_model_name", "gpt-4-vision-preview") 

    payment_methods_list = get_payment_methods(state)
    
    prompt = (
        "Tell me the details of the receipt. Make sure to ALWAYS reply by calling the ReceiptData function.NEVER ask the user to provide additional information.\n"
        f"NEVER reply in any other way than caling the function. if you are not sure about some info make a well educated guess, but ALWAYS call the function.\n"
        f"Choose one of the following payment methods for the 'payment_method' field:\n{', '.join(payment_methods_list)}"
    )

    if "claude" in vision_model_name.lower():
        chat = ChatAnthropic(model=vision_model_name, temperature=0)
    else:
        chat = ChatOpenAI(model=vision_model_name, temperature=0)

    structured_llm = chat.with_structured_output(ReceiptData)

    messages = [
        HumanMessage(
            content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}",
                    },
                },
                {"type": "text", "text": prompt},
            ]
        )
    ]

    response = structured_llm.invoke(messages)

    return response.dict()

def json_parsing_node(state):

    new_state = state.copy()

    image_base64 = state.get("image_base64", "").strip()

    receipt_data = get_receipt_json(image_base64, state)

    new_state["date"] = receipt_data.get("date", None)
    new_state["description"] = receipt_data.get("description", None)
    new_state["amount"] = receipt_data.get("amount", None)
    new_state["vat"] = receipt_data.get("vat", None)
    new_state["business_personal"] = receipt_data.get("business_personal", None)
    new_state["payment_method"] = receipt_data.get("payment_method", None)

    print("json_parsing_node returning:", new_state)

    return new_state
