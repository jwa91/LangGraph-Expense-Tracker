from nodes.imageencoder import image_encoder_node
from nodes.jsonparser import json_parsing_node
from nodes.categorizer import categorizer_node 
from nodes.humancheck import humancheck_node
from nodes.db_entry import db_entry_node
from nodes.correct import correct_node

from helpers.get_payment_methods_and_categories import get_payment_methods, get_categories

from typing import TypedDict, Optional, Dict
from datetime import date
from decimal import Decimal
from langgraph.graph import StateGraph
from dotenv import load_dotenv
from langsmith import Client
import os
from uuid import uuid4

load_dotenv()

unique_id = uuid4().hex[:8]
os.environ["LANGCHAIN_PROJECT"] = f"expense-tracker {unique_id}"

client = Client(api_key=os.environ["LANGSMITH_API_KEY"])

class GraphState(TypedDict):
    user_decision: Optional[list]
    image_base64: Optional[str]
    image_location: Optional[str]
    date: Optional[date]
    category_id: Optional[int]
    description: Optional[str]
    amount: Optional[Decimal]
    vat: Optional[Decimal]
    payment_method_id: Optional[int]
    business_personal: Optional[str]
    category: Optional[str]
    payment_method: Optional[str]
    payment_methods_dict: Optional[Dict[int, str]]
    categories_dict: Optional[Dict[int, str]]
    vision_model_name: Optional[str]
    categorizer_model_name: Optional[str]

def create_graph_state() -> GraphState:
    payment_methods_dict = get_payment_methods()
    categories_dict = get_categories()

    return {
        "user_decision": None,
        "image_base64": None,
        "image_location": None,
        "date": None,
        "category_id": None,
        "description": None,
        "amount": None,
        "vat": None,
        "payment_method_id": None,
        "business_personal": None,
        "category": None,
        "payment_method": None,
        "payment_methods_dict": payment_methods_dict,
        "categories_dict": categories_dict,
        "vision_model_name": "gpt-4-vision-preview",  
        "categorizer_model_name": "gpt-4-turbo",  
    }

def setup_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)

    workflow.add_node("image_encoder", image_encoder_node)
    workflow.add_node("json_parser", json_parsing_node)
    workflow.add_node("categorizer", categorizer_node)
    workflow.add_node("humancheck", humancheck_node)
    workflow.add_edge("image_encoder", "json_parser")
    workflow.add_edge("json_parser", "categorizer")
    workflow.add_edge("categorizer", "humancheck")

    workflow.add_node("db_entry", db_entry_node)
    workflow.add_node("correct", correct_node)

    def decide_humancheck(state):
        if state.get('user_decision') == "accept":
            return "db_entry"
        elif state.get('user_decision') == "change_model":
            return "json_parser"
        elif state.get('user_decision') == "correct":
            return "correct"
        return None

    workflow.add_conditional_edges("humancheck", decide_humancheck, {
        "db_entry": "db_entry",
        "json_parser": "json_parser",
        "correct": "correct"
    })

    workflow.add_edge("correct", "humancheck")

    workflow.set_entry_point("image_encoder")
    workflow.set_finish_point("db_entry")  

    return workflow

def main():
    workflow = setup_workflow()
    app = workflow.compile()

    initial_state = create_graph_state() 

    initial_state["image_location"] = "/Users/jw/developer/expense_tracker/data/walmart-bon.jpeg"
    
    result = app.invoke(initial_state)

    print("Finished run")

if __name__ == "__main__":
    main()
