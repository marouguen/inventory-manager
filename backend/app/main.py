import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api import auth, products,categories,suppliers,stock,dashboard,users

load_dotenv()  # Load from .env file

origins = os.getenv("CORS_ORIGINS", "").split(",")

app = FastAPI()

app.include_router(auth.router)
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers"])
app.include_router(stock.router, prefix="/stock", tags=["Stock"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(users.router) 

# CORS config for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in origins if origin],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Inventory API is running"}
