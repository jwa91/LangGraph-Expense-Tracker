from fastapi import FastAPI
from src.api.category_routes import router as category_router
from src.api.payment_methods_routes import router as payment_methods_router
from src.api.expenses_routes import router as expenses_router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Expense Management API",
    version="1.0.0"
)

app.include_router(category_router)
app.include_router(payment_methods_router)
app.include_router(expenses_router)
