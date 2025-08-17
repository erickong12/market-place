import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database.base import Base
from app.database.session import engine
from app.core.exception import http_exception_handler
from app.core.middleware import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.routers import admin, auth, cart, order, product, seller_inventory

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_exception_handler(Exception, http_exception_handler)
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)
app.add_middleware(AuthMiddleware)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(product.router)
app.include_router(seller_inventory.router)
app.include_router(cart.router)
app.include_router(order.router)

static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

if not os.path.exists(static_path):
    os.makedirs(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")
