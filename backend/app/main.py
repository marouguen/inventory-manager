import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api import auth, products, categories, suppliers, stock, dashboard, users

load_dotenv()  # Load environment variables from .env

origins = os.getenv("CORS_ORIGINS", "").split(",")

app = FastAPI()

# API router with /api prefix
api_router = APIRouter(prefix="/api")

# Include all API sub-routers under /api
api_router.include_router(auth.router)
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers"])
api_router.include_router(stock.router, prefix="/stock", tags=["Stock"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(users.router)

app.include_router(api_router)

# CORS config for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in origins if origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Inventory API is running"}
