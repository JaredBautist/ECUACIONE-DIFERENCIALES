"""Compatibilidad: expone la app FastAPI desde el backend modular."""
import sys
from pathlib import Path

# Agregar la carpeta scripts al path para importar backend/
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

from backend.app import app  # type: ignore

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
