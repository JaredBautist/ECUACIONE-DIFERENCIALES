# Instrucciones rápidas para el backend

1. Instala las dependencias de Python desde la raíz del repo:
   ```bash
   pip install -r scripts/requirements.txt
   ```
2. Arranca el servidor FastAPI:
   ```bash
   python3 scripts/python_backend_server.py
   ```
   También puedes usar uvicorn directo: `uvicorn scripts.python_backend_server:app --reload --port 8000`.
3. Configura la URL para el frontend con `PYTHON_BACKEND_URL` (por defecto `http://localhost:8000`).
4. Notación soportada:
   - Potencias sobre funciones: `sin^2(x)` o `sin(x)^2`
   - Multiplicación implícita: `x(y+1)` se interpreta como `x*(y+1)`
   - Formato exacto: `M dx + N dy = 0`
   - Condiciones iniciales: añade después de la ecuación separadas por `;` o salto de línea, ej: `dy/dx = x*y; y(0)=2; y'(0)=1`
5. Funciones disponibles sin pasos extra: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `asin`, `acos`, `atan`, `sec`, `csc`, `cot`, `sinh`, `cosh`, `tanh`, además de `pi` y `E`.
6. Si recibes un 400 al resolver, revisa la notación: agrega paréntesis, usa `^` para potencias y confirma que la función esté en la lista anterior.
7. Endpoints nuevos:
   - `POST /solve` (simbólico y numérico: Euler, RK4; soporta CI).
   - `POST /solve/system` para sistemas (numérico o simbólico si SymPy lo resuelve).
   - `POST /validate` usa Qwen (si QWEN_API_KEY está configurada) para validar soluciones.
