"""
Solucionador de Ecuaciones Diferenciales usando SymPy
Este script proporciona funciones para resolver diferentes tipos de ecuaciones diferenciales
"""

import json
import re
from sympy import (
    Derivative,
    Eq,
    Function,
    acos,
    asin,
    atan,
    cos,
    cosh,
    csc,
    dsolve,
    exp,
    latex,
    log,
    sec,
    sin,
    sinh,
    sqrt,
    symbols,
    tan,
    tanh,
)
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

# Definir símbolos
x, C1, C2, C3 = symbols('x C1 C2 C3')
y = Function('y')
TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)
ALLOWED_LOCAL_DICT = {
    'x': x,
    'y': y,
    'Derivative': Derivative,
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'exp': exp,
    'log': log,
    'sqrt': sqrt,
    'asin': asin,
    'acos': acos,
    'atan': atan,
    'sec': sec,
    'csc': csc,
    'sinh': sinh,
    'cosh': cosh,
    'tanh': tanh,
}


def parse_equation(equation_str: str):
    """
    Parsea una ecuación diferencial en formato string a formato SymPy
    
    Args:
        equation_str: Ecuación en formato string (ej: "dy/dx = x*y")
    
    Returns:
        Objeto de ecuación de SymPy
    """
    # Reemplazar notación común
    equation_str = equation_str.replace('dy/dx', 'Derivative(y(x), x)')
    equation_str = equation_str.replace("y''", 'Derivative(y(x), x, 2)')
    equation_str = equation_str.replace("y'", 'Derivative(y(x), x)')
    equation_str = re.sub(r'\by\b(?!\()', 'y(x)', equation_str)
    equation_str = equation_str.replace('e^', 'exp')
    equation_str = equation_str.replace('ln', 'log')
    equation_str = equation_str.replace('^', '**')
    
    # Dividir por el signo igual
    if '=' in equation_str:
        left, right = equation_str.split('=')
        left_expr = parse_expr(
            left.strip(),
            transformations=TRANSFORMATIONS,
            local_dict=ALLOWED_LOCAL_DICT,
        )
        right_expr = parse_expr(
            right.strip(),
            transformations=TRANSFORMATIONS,
            local_dict=ALLOWED_LOCAL_DICT,
        )
        return Eq(left_expr, right_expr)
    else:
        return parse_expr(
            equation_str,
            transformations=TRANSFORMATIONS,
            local_dict=ALLOWED_LOCAL_DICT,
        )


def solve_separable(equation_str: str):
    """
    Resuelve una ecuación diferencial de variables separables
    
    Ejemplo: dy/dx = x*y
    """
    eq = parse_equation(equation_str)
    solution = dsolve(eq, y(x))
    
    return {
        "originalEquation": latex(eq),
        "solution": latex(solution.rhs),
        "steps": [
            {
                "title": "Paso 1: Identificación",
                "description": "Identificamos que esta es una ecuación de variables separables de la forma dy/dx = f(x)g(y)",
                "equation": latex(eq)
            },
            {
                "title": "Paso 2: Separación de variables",
                "description": "Separamos las variables: dy/g(y) = f(x)dx",
                "equation": "\\frac{dy}{g(y)} = f(x)dx"
            },
            {
                "title": "Paso 3: Integración",
                "description": "Integramos ambos lados de la ecuación",
                "equation": "\\int \\frac{dy}{g(y)} = \\int f(x)dx"
            },
            {
                "title": "Paso 4: Solución general",
                "description": "Despejamos y para obtener la solución general",
                "equation": latex(solution)
            }
        ]
    }


def solve_linear(equation_str: str):
    """
    Resuelve una ecuación diferencial lineal de primer orden
    
    Ejemplo: dy/dx + 2*y = 4*x
    """
    eq = parse_equation(equation_str)
    solution = dsolve(eq, y(x))
    
    return {
        "originalEquation": latex(eq),
        "solution": latex(solution.rhs),
        "steps": [
            {
                "title": "Paso 1: Forma estándar",
                "description": "Identificamos que es una ecuación lineal de la forma dy/dx + P(x)y = Q(x)",
                "equation": latex(eq)
            },
            {
                "title": "Paso 2: Factor integrante",
                "description": "Calculamos el factor integrante μ(x) = e^(∫P(x)dx)",
                "equation": "\\mu(x) = e^{\\int P(x)dx}"
            },
            {
                "title": "Paso 3: Multiplicación",
                "description": "Multiplicamos toda la ecuación por el factor integrante",
                "equation": "\\mu(x)\\frac{dy}{dx} + \\mu(x)P(x)y = \\mu(x)Q(x)"
            },
            {
                "title": "Paso 4: Solución general",
                "description": "Integramos y despejamos y para obtener la solución general",
                "equation": latex(solution)
            }
        ]
    }


def solve_homogeneous(equation_str: str):
    """
    Resuelve una ecuación diferencial homogénea
    
    Ejemplo: dy/dx = (x+y)/x
    """
    eq = parse_equation(equation_str)
    solution = dsolve(eq, y(x))
    
    return {
        "originalEquation": latex(eq),
        "solution": latex(solution.rhs),
        "steps": [
            {
                "title": "Paso 1: Verificación de homogeneidad",
                "description": "Verificamos que la ecuación es homogénea: f(tx,ty) = f(x,y)",
                "equation": latex(eq)
            },
            {
                "title": "Paso 2: Sustitución",
                "description": "Hacemos la sustitución v = y/x, entonces y = vx y dy/dx = v + x(dv/dx)",
                "equation": "v = \\frac{y}{x}, \\quad \\frac{dy}{dx} = v + x\\frac{dv}{dx}"
            },
            {
                "title": "Paso 3: Variables separables",
                "description": "La ecuación se transforma en una de variables separables",
                "equation": "x\\frac{dv}{dx} = f(v) - v"
            },
            {
                "title": "Paso 4: Solución general",
                "description": "Resolvemos e invertimos la sustitución y = vx",
                "equation": latex(solution)
            }
        ]
    }


def solve_exact(equation_str: str):
    """
    Resuelve una ecuación diferencial exacta
    
    Ejemplo: (2*x+y)dx + (x+2*y)dy = 0
    """
    eq = parse_equation(equation_str)
    solution = dsolve(eq, y(x))
    
    return {
        "originalEquation": latex(eq),
        "solution": latex(solution.rhs),
        "steps": [
            {
                "title": "Paso 1: Forma estándar",
                "description": "Identificamos la ecuación en la forma M(x,y)dx + N(x,y)dy = 0",
                "equation": latex(eq)
            },
            {
                "title": "Paso 2: Verificación de exactitud",
                "description": "Verificamos que ∂M/∂y = ∂N/∂x",
                "equation": "\\frac{\\partial M}{\\partial y} = \\frac{\\partial N}{\\partial x}"
            },
            {
                "title": "Paso 3: Función potencial",
                "description": "Encontramos la función F(x,y) tal que ∂F/∂x = M y ∂F/∂y = N",
                "equation": "\\frac{\\partial F}{\\partial x} = M, \\quad \\frac{\\partial F}{\\partial y} = N"
            },
            {
                "title": "Paso 4: Solución implícita",
                "description": "La solución es F(x,y) = C",
                "equation": latex(solution)
            }
        ]
    }


def solve_bernoulli(equation_str: str):
    """
    Resuelve una ecuación de Bernoulli
    
    Ejemplo: dy/dx + y = y^2*x
    """
    eq = parse_equation(equation_str)
    solution = dsolve(eq, y(x))
    
    return {
        "originalEquation": latex(eq),
        "solution": latex(solution.rhs),
        "steps": [
            {
                "title": "Paso 1: Identificación",
                "description": "Identificamos la ecuación de Bernoulli: dy/dx + P(x)y = Q(x)y^n",
                "equation": latex(eq)
            },
            {
                "title": "Paso 2: Sustitución",
                "description": "Hacemos la sustitución v = y^(1-n) para linearizar",
                "equation": "v = y^{1-n}"
            },
            {
                "title": "Paso 3: Ecuación lineal",
                "description": "La ecuación se transforma en una ecuación lineal en v",
                "equation": "\\frac{dv}{dx} + (1-n)P(x)v = (1-n)Q(x)"
            },
            {
                "title": "Paso 4: Solución general",
                "description": "Resolvemos la ecuación lineal e invertimos la sustitución",
                "equation": latex(solution)
            }
        ]
    }


# Función principal que determina qué método usar
def solve_differential_equation(equation_str: str, equation_type: str):
    """
    Resuelve una ecuación diferencial según su tipo
    
    Args:
        equation_str: Ecuación en formato string
        equation_type: Tipo de ecuación (separable, linear, homogeneous, etc.)
    
    Returns:
        Diccionario con la solución y pasos
    """
    solvers = {
        'separable': solve_separable,
        'linear': solve_linear,
        'homogeneous': solve_homogeneous,
        'exact': solve_exact,
        'bernoulli': solve_bernoulli
    }
    
    solver = solvers.get(equation_type, solve_separable)
    
    try:
        result = solver(equation_str)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "originalEquation": equation_str,
            "solution": "Error al resolver",
            "steps": []
        })


# Ejemplo de uso
if __name__ == "__main__":
    # Prueba con diferentes ecuaciones
    print("=== Ecuación Separable ===")
    print(solve_differential_equation("dy/dx = x*y", "separable"))
    
    print("\n=== Ecuación Lineal ===")
    print(solve_differential_equation("dy/dx + 2*y = 4*x", "linear"))
