import re
from typing import Dict, List, Tuple

from sympy import (
    Derivative,
    Function,
    symbols,
    sin,
    cos,
    tan,
    exp,
    log,
    sqrt,
    asin,
    acos,
    atan,
    sec,
    csc,
    cot,
    sinh,
    cosh,
    tanh,
    pi,
    E,
)
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

# Transformaciones y diccionario de símbolos/funciones permitidas
TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)
x = symbols("x")
y_func = Function("y")

ALLOWED_FUNCTIONS = {
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "exp": exp,
    "log": log,
    "sqrt": sqrt,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    "sec": sec,
    "csc": csc,
    "cot": cot,
    "sinh": sinh,
    "cosh": cosh,
    "tanh": tanh,
    "pi": pi,
    "E": E,
}

LOCAL_DICT = {"x": x, "y": y_func, "Derivative": Derivative}
LOCAL_DICT.update(ALLOWED_FUNCTIONS)


def normalize_equation(raw_equation: str) -> Tuple[str, List[str]]:
    """
    Normaliza la ecuación y separa condiciones iniciales.
    Separadores aceptados: ';', saltos de línea o coma seguida de y(.
    """
    if not raw_equation:
        raise ValueError("Ecuación vacía")

    parts = re.split(r"[;\n]+|,(?=\s*[a-zA-Z]+\s*(\(|'))", raw_equation)
    segments = [seg.strip() for seg in parts if seg and seg.strip()]
    if not segments:
        raise ValueError("No se encontró una ecuación en la entrada.")

    equation_str, *ic_segments = segments

    eq = (
        equation_str.replace(" ", "")
        .replace("dy/dx", "Derivative(y(x),x)")
        .replace("y''", "Derivative(y(x),x,2)")
        .replace("y'", "Derivative(y(x),x)")
        .replace("^", "**")
    )
    # y -> y(x) cuando no está en modo función
    eq = re.sub(r"\by\b(?!\()", "y(x)", eq)

    # Exactas: M dx + N dy = 0  -> Derivative(y,x) = -M/N
    match = re.match(r"^(?P<M>.*?)dx\+(?P<N>.*?)dy=0$", eq, re.IGNORECASE)
    if match:
        M = match.group("M")
        N = match.group("N")
        eq = f"Derivative(y(x),x)=-({M})/({N})"

    return eq, ic_segments


def parse_sympy_expression(expr: str):
    return parse_expr(expr, transformations=TRANSFORMATIONS, local_dict=LOCAL_DICT)


def parse_equation(expr: str):
    if "=" in expr:
        left, right = expr.split("=")
        return parse_sympy_expression(left), parse_sympy_expression(right)
    return parse_sympy_expression(expr), None


def parse_initial_conditions(ic_segments: List[str]) -> Dict:
    """
    Convierte CI en diccionario para dsolve.
    Soporta y(x0)=y0, y'(x0)=y1, y''(x0)=y2 y variantes para otras funciones (y1, y2, etc.).
    """
    ics = {}
    pattern = re.compile(
        r"^(?P<var>[a-zA-Z]\w*)(?P<prime>'{0,3})\((?P<x0>[^)]+)\)=(?P<val>.+)$"
    )
    for raw_ic in ic_segments:
        cleaned = raw_ic.replace(" ", "")
        m = pattern.match(cleaned)
        if not m:
            raise ValueError(f"Condición inicial no reconocida: {raw_ic}")
        var_name = m.group("var")
        order = len(m.group("prime"))
        x0_expr = parse_sympy_expression(m.group("x0"))
        val_expr = parse_sympy_expression(m.group("val"))
        func = Function(var_name)

        if order == 0:
            key = func(x0_expr)
        elif order == 1:
            key = func(x).diff(x).subs(x, x0_expr)
        elif order == 2:
            key = func(x).diff(x, 2).subs(x, x0_expr)
        elif order == 3:
            key = func(x).diff(x, 3).subs(x, x0_expr)
        else:
            raise ValueError(f"Orden de derivada no soportado en CI: {raw_ic}")

        ics[key] = val_expr
    return ics
