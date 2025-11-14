# Backend Python - DiffEQ Solver

Este proyecto utiliza un backend en Python para resolver ecuaciones diferenciales de manera precisa usando SymPy.

## Configuración del Backend

### 1. Instalar dependencias de Python

\`\`\`bash
pip install -r scripts/requirements.txt
\`\`\`

### 2. Iniciar el servidor backend

\`\`\`bash
cd scripts
python python_backend_server.py
\`\`\`

O usando uvicorn directamente:

\`\`\`bash
uvicorn scripts.python_backend_server:app --reload --port 8000
\`\`\`

El servidor estará disponible en: `http://localhost:8000`

### 3. Documentación de la API

Una vez iniciado el servidor, puedes acceder a la documentación interactiva en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Estructura del Backend

### `de_solver.py`
Script standalone con funciones para resolver diferentes tipos de ecuaciones diferenciales.

**Funciones principales:**
- `solve_separable()` - Ecuaciones de variables separables
- `solve_linear()` - Ecuaciones lineales de primer orden
- `solve_homogeneous()` - Ecuaciones homogéneas
- `solve_exact()` - Ecuaciones exactas
- `solve_bernoulli()` - Ecuaciones de Bernoulli

### `python_backend_server.py`
Servidor FastAPI que expone endpoints REST para el frontend.

**Endpoints:**
- `POST /solve` - Resolver una ecuación diferencial
- `GET /` - Información del API
- `GET /health` - Estado del servidor

## Uso del Backend

### Ejemplo de request:

\`\`\`bash
curl -X POST "http://localhost:8000/solve" \
  -H "Content-Type: application/json" \
  -d '{
    "equation": "dy/dx = x*y",
    "equation_type": "separable"
  }'
\`\`\`

### Ejemplo de response:

\`\`\`json
{
  "originalEquation": "\\frac{dy}{dx} = xy",
  "solution": "C_1 e^{\\frac{x^2}{2}}",
  "steps": [
    {
      "title": "Paso 1: Identificación del tipo",
      "description": "...",
      "equation": "..."
    }
  ]
}
\`\`\`

## Ventajas del Backend en Python

1. **SymPy**: Librería especializada en matemáticas simbólicas
2. **Precisión**: Soluciones matemáticamente exactas
3. **Facilidad de mantenimiento**: Código Python claro y legible
4. **Escalabilidad**: Fácil agregar nuevos tipos de ecuaciones
5. **Documentación**: API auto-documentada con FastAPI

## Tipos de Ecuaciones Soportados

- ✅ Variables Separables
- ✅ Lineales de Primer Orden
- ✅ Homogéneas
- ✅ Exactas
- ✅ Bernoulli
- 🔄 Coeficientes Constantes (en desarrollo)
- 🔄 Factor Integrante (en desarrollo)

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

\`\`\`env
PYTHON_BACKEND_URL=http://localhost:8000
\`\`\`

## Notas de Desarrollo

- El backend usa SymPy para resolución simbólica exacta
- Cada tipo de ecuación tiene su generador de pasos personalizado
- Los pasos incluyen descripciones detalladas en español
- El renderizado LaTeX es compatible con KaTeX en el frontend
