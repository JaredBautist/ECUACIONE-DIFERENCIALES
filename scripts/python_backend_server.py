"""
Servidor backend en Python para resolver ecuaciones diferenciales
Usa FastAPI para crear una API REST que el frontend puede consumir
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sympy import symbols, Function, dsolve, Eq, latex, sin, cos, exp, log, sqrt
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

app = FastAPI(title="DiffEQ Solver API", version="1.0.0")

# Configurar CORS para permitir requests del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definir símbolos
x = symbols('x')
y = Function('y')


class EquationRequest(BaseModel):
    equation: str
    equation_type: str


class SolutionResponse(BaseModel):
    originalEquation: str
    solution: str
    steps: list


def preprocess_equation(eq_str: str) -> str:
    """
    Preprocesa la ecuación para que SymPy pueda parsearla correctamente
    """
    # Reemplazar notaciones comunes
    eq_str = eq_str.replace(' ', '')
    eq_str = eq_str.replace("dy/dx", "Derivative(y(x),x)")
    eq_str = eq_str.replace("y'", "Derivative(y(x),x)")
    eq_str = eq_str.replace("y''", "Derivative(y(x),x,2)")
    
    # Reemplazar y por y(x), pero no si ya está como y(x)
    eq_str = re.sub(r'\by\b(?!\()', 'y(x)', eq_str)
    
    # Reemplazar funciones comunes
    eq_str = eq_str.replace('e^', 'exp')
    eq_str = eq_str.replace('ln', 'log')
    eq_str = eq_str.replace('sqrt', 'sqrt')
    
    return eq_str


def create_steps_separable(original_eq, solution_eq):
    """Genera pasos para ecuaciones de variables separables"""
    return [
        {
            "title": "Paso 1: Identificación del tipo",
            "description": "Identificamos que esta es una ecuación de variables separables de la forma dy/dx = f(x)g(y), donde podemos separar las variables x e y en lados opuestos.",
            "equation": original_eq
        },
        {
            "title": "Paso 2: Separación de variables",
            "description": "Reorganizamos la ecuación para separar las variables: llevamos todos los términos con y al lado izquierdo y todos los términos con x al lado derecho.",
            "equation": "\\frac{1}{g(y)}dy = f(x)dx"
        },
        {
            "title": "Paso 3: Integración de ambos lados",
            "description": "Integramos ambos lados de la ecuación. La integral del lado izquierdo es respecto a y, y la del lado derecho respecto a x.",
            "equation": "\\int \\frac{1}{g(y)}dy = \\int f(x)dx"
        },
        {
            "title": "Paso 4: Solución general",
            "description": "Después de integrar, despejamos y para obtener la solución general. La constante C representa la familia de soluciones.",
            "equation": solution_eq
        }
    ]


def create_steps_linear(original_eq, solution_eq):
    """Genera pasos para ecuaciones lineales de primer orden"""
    return [
        {
            "title": "Paso 1: Forma estándar",
            "description": "Identificamos que es una ecuación lineal de primer orden de la forma dy/dx + P(x)y = Q(x). Reordenamos si es necesario.",
            "equation": original_eq
        },
        {
            "title": "Paso 2: Cálculo del factor integrante",
            "description": "Calculamos el factor integrante μ(x) = e^(∫P(x)dx). Este factor nos permitirá convertir el lado izquierdo en una derivada de producto.",
            "equation": "\\mu(x) = e^{\\int P(x)dx}"
        },
        {
            "title": "Paso 3: Multiplicación por el factor integrante",
            "description": "Multiplicamos toda la ecuación por μ(x). El lado izquierdo se convierte en d/dx[μ(x)y].",
            "equation": "\\frac{d}{dx}[\\mu(x)y] = \\mu(x)Q(x)"
        },
        {
            "title": "Paso 4: Integración y solución",
            "description": "Integramos ambos lados y despejamos y. Dividimos por μ(x) para obtener la solución general.",
            "equation": solution_eq
        }
    ]


def create_steps_homogeneous(original_eq, solution_eq):
    """Genera pasos para ecuaciones homogéneas"""
    return [
        {
            "title": "Paso 1: Verificación de homogeneidad",
            "description": "Verificamos que la ecuación es homogénea: si reemplazamos x por tx y y por ty, obtenemos t^n veces la función original, donde n es el grado de homogeneidad.",
            "equation": original_eq
        },
        {
            "title": "Paso 2: Sustitución v = y/x",
            "description": "Realizamos la sustitución v = y/x, lo que implica y = vx. Derivando: dy/dx = v + x(dv/dx).",
            "equation": "v = \\frac{y}{x}, \\quad y = vx, \\quad \\frac{dy}{dx} = v + x\\frac{dv}{dx}"
        },
        {
            "title": "Paso 3: Ecuación en variables separables",
            "description": "Sustituimos en la ecuación original. La ecuación resultante es de variables separables en v y x.",
            "equation": "x\\frac{dv}{dx} = g(v)"
        },
        {
            "title": "Paso 4: Solución y reversión",
            "description": "Resolvemos la ecuación separable, integramos y luego revertimos la sustitución v = y/x para obtener y en términos de x.",
            "equation": solution_eq
        }
    ]


def create_steps_exact(original_eq, solution_eq):
    """Genera pasos para ecuaciones exactas"""
    return [
        {
            "title": "Paso 1: Forma estándar M(x,y)dx + N(x,y)dy = 0",
            "description": "Identificamos M(x,y) y N(x,y) en la ecuación de la forma M(x,y)dx + N(x,y)dy = 0.",
            "equation": original_eq
        },
        {
            "title": "Paso 2: Prueba de exactitud",
            "description": "Verificamos que la ecuación es exacta comprobando que ∂M/∂y = ∂N/∂x. Si son iguales, la ecuación es exacta.",
            "equation": "\\frac{\\partial M}{\\partial y} = \\frac{\\partial N}{\\partial x}"
        },
        {
            "title": "Paso 3: Búsqueda de la función potencial F(x,y)",
            "description": "Buscamos una función F(x,y) tal que ∂F/∂x = M y ∂F/∂y = N. Integramos M respecto a x y N respecto a y.",
            "equation": "F(x,y) = \\int M(x,y)dx = \\int N(x,y)dy"
        },
        {
            "title": "Paso 4: Solución implícita",
            "description": "La solución de la ecuación diferencial es F(x,y) = C, donde C es una constante arbitraria.",
            "equation": solution_eq
        }
    ]


def create_steps_bernoulli(original_eq, solution_eq):
    """Genera pasos para ecuaciones de Bernoulli"""
    return [
        {
            "title": "Paso 1: Identificación de Bernoulli",
            "description": "Identificamos la ecuación de Bernoulli de la forma dy/dx + P(x)y = Q(x)y^n, donde n ≠ 0,1.",
            "equation": original_eq
        },
        {
            "title": "Paso 2: Sustitución de linearización",
            "description": "Realizamos la sustitución v = y^(1-n) para convertir la ecuación no lineal en una ecuación lineal en v.",
            "equation": "v = y^{1-n}, \\quad \\frac{dv}{dx} = (1-n)y^{-n}\\frac{dy}{dx}"
        },
        {
            "title": "Paso 3: Ecuación lineal resultante",
            "description": "Dividimos la ecuación original por y^n y sustituimos para obtener una ecuación lineal en v.",
            "equation": "\\frac{dv}{dx} + (1-n)P(x)v = (1-n)Q(x)"
        },
        {
            "title": "Paso 4: Solución y reversión",
            "description": "Resolvemos la ecuación lineal usando el factor integrante, luego revertimos la sustitución v = y^(1-n).",
            "equation": solution_eq
        }
    ]


@app.post("/solve", response_model=SolutionResponse)
async def solve_equation(request: EquationRequest):
    """
    Endpoint principal para resolver ecuaciones diferenciales
    """
    try:
        # Preprocesar la ecuación
        eq_str = preprocess_equation(request.equation)
        
        # Parsear la ecuación
        if '=' in eq_str:
            left, right = eq_str.split('=')
            left_expr = parse_expr(left.strip())
            right_expr = parse_expr(right.strip())
            eq = Eq(left_expr, right_expr)
        else:
            eq = parse_expr(eq_str)
        
        # Resolver la ecuación
        solution = dsolve(eq, y(x))
        
        # Obtener las ecuaciones en LaTeX
        original_latex = latex(eq)
        
        # Manejar diferentes formatos de solución
        if hasattr(solution, 'rhs'):
            solution_latex = latex(solution.rhs)
        elif isinstance(solution, list) and len(solution) > 0:
            solution_latex = latex(solution[0].rhs)
        else:
            solution_latex = latex(solution)
        
        # Crear pasos según el tipo de ecuación
        steps_generators = {
            'separable': create_steps_separable,
            'linear': create_steps_linear,
            'homogeneous': create_steps_homogeneous,
            'exact': create_steps_exact,
            'bernoulli': create_steps_bernoulli,
        }
        
        step_generator = steps_generators.get(
            request.equation_type,
            create_steps_separable
        )
        steps = step_generator(original_latex, solution_latex)
        
        return SolutionResponse(
            originalEquation=original_latex,
            solution=solution_latex,
            steps=steps
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al resolver la ecuación: {str(e)}"
        )


@app.get("/")
async def root():
    """Endpoint de bienvenida"""
    return {
        "message": "DiffEQ Solver API",
        "version": "1.0.0",
        "endpoints": {
            "/solve": "POST - Resolver ecuación diferencial",
            "/docs": "GET - Documentación interactiva"
        }
    }


@app.get("/health")
async def health_check():
    """Endpoint de salud del servidor"""
    return {"status": "healthy"}


# Para ejecutar: uvicorn python_backend_server:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
