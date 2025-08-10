import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database.base import Base
from app.database.session import engine
from app.core.exception import http_exception_handler
from app.core.middleware import AuthMiddleware
from app.routers import auth, product, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(Exception, http_exception_handler)

app.add_middleware(AuthMiddleware)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)
# app.include_router(inventory.router, prefix="/inventory")
# app.include_router(cart.router, prefix="/cart")
# app.include_router(order.router, prefix="/orders")
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

if not os.path.exists(static_path):
    os.makedirs(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")
