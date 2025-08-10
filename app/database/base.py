import pkgutil
import importlib
from pathlib import Path
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Auto-import all modules in app/models
models_path = Path(__file__).parent.parent / "models"
for _, module_name, _ in pkgutil.iter_modules([str(models_path)]):
    importlib.import_module(f"app.models.{module_name}")
