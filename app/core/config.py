from os import environ as env

SECRET_KEY = env.get("SECRET_KEY", "your_secret_key")
ALGORITHM = env.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = float(env.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
DATABASE_URL = env.get("DATABASE_URL")
UPLOAD_DIR = env.get("UPLOAD_DIR", "static/products")
