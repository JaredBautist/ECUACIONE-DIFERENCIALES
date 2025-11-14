# DiffEQ Solver - Resolvedor de Ecuaciones Diferenciales

Una aplicación web moderna y elegante para resolver ecuaciones diferenciales con explicaciones paso a paso, inspirada en Symbolab y Photomath.

## Características

- **9 tipos de ecuaciones diferenciales** soportadas
- **Soluciones paso a paso** con explicaciones detalladas
- **Renderizado matemático hermoso** usando KaTeX/LaTeX
- **12 ejercicios de ejemplo** organizados por dificultad
- **Backend Python potente** usando SymPy para cálculos precisos
- **Interfaz moderna** con diseño inspirado en Symbolab

## Tipos de Ecuaciones Soportadas

1. Variables Separables
2. Homogéneas
3. Exactas
4. Lineales de Primer Orden
5. Ecuaciones de Bernoulli
6. Reducibles a Primer Orden
7. Coeficientes Constantes
8. Coeficientes Indeterminados
9. Factor Integrante

## Configuración del Proyecto

### 1. Configurar el Backend Python

El backend Python es necesario para resolver las ecuaciones diferenciales.

#### Instalar dependencias:

\`\`\`bash
cd scripts
pip install -r requirements.txt
\`\`\`

#### Ejecutar el servidor:

\`\`\`bash
python python_backend_server.py
\`\`\`

O usando uvicorn directamente:

\`\`\`bash
uvicorn python_backend_server:app --reload --port 8000
\`\`\`

El servidor estará disponible en `http://localhost:8000`

### 2. Configurar Variables de Entorno

Asegúrate de que la variable de entorno `PYTHON_BACKEND_URL` esté configurada:

\`\`\`bash
PYTHON_BACKEND_URL=http://localhost:8000
\`\`\`

Si despliegas en producción, actualiza esta URL al endpoint de tu servidor Python.

### 3. Ejecutar el Frontend

El frontend Next.js se ejecuta automáticamente en v0. Si lo ejecutas localmente:

\`\`\`bash
npm install
npm run dev
\`\`\`

## Estructura del Proyecto

\`\`\`
├── app/
│   ├── page.tsx                 # Página principal
│   ├── layout.tsx              # Layout de la aplicación
│   └── globals.css             # Estilos globales y tema
├── components/
│   ├── differential-equation-solver.tsx  # Componente principal
│   ├── example-exercises.tsx             # Ejercicios de ejemplo
│   ├── math-display.tsx                  # Display de ecuaciones LaTeX
│   └── solution-steps.tsx                # Pasos de la solución
├── lib/
│   └── de-solver.ts            # Cliente que conecta con Python backend
└── scripts/
    ├── python_backend_server.py  # Servidor FastAPI
    └── requirements.txt          # Dependencias Python
\`\`\`

## Uso de la Aplicación

1. **Selecciona el tipo de ecuación** diferencial que deseas resolver
2. **Ingresa tu ecuación** usando notación estándar:
   - Derivadas: `dy/dx`, `y'`, `y''`
   - Potencias: `x^2`, `y^3`
   - Funciones: `sin(x)`, `cos(x)`, `exp(x)`, `ln(x)`, `sqrt(x)`
3. **Haz clic en "Resolver Ecuación"** o presiona Enter
4. **Explora los resultados**:
   - Pestaña "Resultado Final": Muestra la solución completa
   - Pestaña "Paso a Paso": Muestra el proceso detallado

## Ejercicios de Ejemplo

La aplicación incluye 12 ejercicios precargados organizados en tres niveles:

- **Básicos**: Ecuaciones fundamentales para aprender los conceptos
- **Intermedios**: Ecuaciones más complejas con múltiples pasos
- **Avanzados**: Desafíos que requieren técnicas avanzadas

Haz clic en el botón ▶️ junto a cualquier ejercicio para cargarlo automáticamente.

## Ejemplos de Notación

### Derivadas
\`\`\`
dy/dx = x*y
y' + 2*y = 4*x
y'' - y = 0
\`\`\`

### Operaciones
\`\`\`
dy/dx = x^2 + y^2
dy/dx = sqrt(x)*y
dy/dx = exp(x)*sin(y)
\`\`\`

### Ecuaciones Exactas
\`\`\`
(2*x + y)dx + (x + 2*y)dy = 0
\`\`\`

## Tecnologías Utilizadas

### Frontend
- **Next.js 16** con App Router
- **React 19** con Server Components
- **TailwindCSS v4** para estilos
- **shadcn/ui** componentes
- **KaTeX** para renderizado matemático

### Backend
- **Python 3.8+**
- **FastAPI** para la API REST
- **SymPy** para cálculos simbólicos
- **Uvicorn** como servidor ASGI

## API del Backend

### POST /solve

Resuelve una ecuación diferencial.

**Request:**
\`\`\`json
{
  "equation": "dy/dx = x*y",
  "equation_type": "separable"
}
\`\`\`

**Response:**
\`\`\`json
{
  "originalEquation": "\\frac{dy}{dx} = xy",
  "solution": "y = C e^{\\frac{x^2}{2}}",
  "steps": [
    {
      "title": "Paso 1: ...",
      "description": "...",
      "equation": "..."
    }
  ]
}
\`\`\`

## Solución de Problemas

### El backend Python no se conecta

1. Verifica que el servidor Python esté corriendo en el puerto 8000
2. Revisa la variable de entorno `PYTHON_BACKEND_URL`
3. Verifica que no haya conflictos de puerto con otras aplicaciones

### Error al parsear la ecuación

1. Usa la notación correcta (ver ejemplos arriba)
2. Asegúrate de usar `dy/dx` para derivadas
3. Verifica que todos los paréntesis estén balanceados

### Las ecuaciones no se renderizan correctamente

1. Verifica que KaTeX esté cargado correctamente
2. Revisa la consola del navegador para errores de sintaxis LaTeX

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## Licencia

MIT License - siéntete libre de usar este proyecto para aprendizaje y desarrollo.

## Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**¡Disfruta resolviendo ecuaciones diferenciales!** 📐✨
