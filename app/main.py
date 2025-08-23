import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import AuthMiddleware
from app.database.base import Base
from app.database.session import engine
from app.core.exception import http_exception_handler
from app.routers import admin, auth, cart, order, product, seller_inventory
from app.task.auto_cancel import start_scheduler

# --- Create DB tables ---
Base.metadata.create_all(bind=engine)

# --- FastAPI app ---
app = FastAPI()

# --- Scheduled tasks ---
app.on_event("startup")(start_scheduler)

# --- Custom global exception handler with CORS headers ---
app.add_exception_handler(Exception, http_exception_handler)

# --- Middleware! ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://market-place-front-end-production.up.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

# --- Routers ---
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(product.router)
app.include_router(seller_inventory.router)
app.include_router(cart.router)
app.include_router(order.router)

# --- Static files ---
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if not os.path.exists(static_path):
    os.makedirs(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")
