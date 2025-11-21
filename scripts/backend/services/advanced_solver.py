"""
Adaptación del ODESolver del backend de Carlos para uso como servicio en FastAPI.
Incluye métodos de primer orden (separable, homogéneas, exactas, lineales, Bernoulli,
factor integrante) y segundo orden (coeficientes constantes, reducibles), con soporte
de condiciones iniciales y salidas en texto/LaTeX.
"""

import re
import sympy as sp
from sympy import (
    Eq,
    Function,
    Symbol,
    symbols,
    diff,
    dsolve,
    exp,
    integrate,
    latex,
    simplify,
    sqrt,
)
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


class ODESolver:
    def __init__(self):
        self.x = symbols("x")
        self.y = Function("y")
        self.C1, self.C2 = symbols("C1 C2")
        self.parse_locals = {
            "x": self.x,
            "y": self.y,
            "Derivative": sp.Derivative,
            "E": sp.E,
            "e": sp.E,
            "pi": sp.pi,
            "PI": sp.pi,
            "exp": sp.exp,
            "sqrt": sp.sqrt,
            "log": sp.log,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,
            "sec": sp.sec,
            "csc": sp.csc,
            "cot": sp.cot,
            "sinh": sp.sinh,
            "cosh": sp.cosh,
            "tanh": sp.tanh,
        }
        self.transformations = standard_transformations + (implicit_multiplication_application,)

    # ------------------ Utilidades de formato ------------------ #
    def format_solution(self, solution):
        sol_str = str(solution)
        if sol_str.startswith("Eq(y(x), "):
            rhs = sol_str[9:-1]
            sol_str = f"y(x) = {rhs}"
        sol_str = sol_str.replace("**", "^")
        sol_str = sol_str.replace("*", "·")
        sol_str = sol_str.replace("exp(", "e^(")
        sol_str = sol_str.replace("log(", "ln(")
        sol_str = sol_str.replace("sqrt(", "√(")
        return sol_str

    def get_latex_solution(self, solution):
        try:
            if isinstance(solution, sp.Eq):
                lhs = latex(solution.lhs)
                rhs = latex(solution.rhs)
                return f"{lhs} = {rhs}"
            return latex(solution)
        except Exception:
            return str(solution)

    # ------------------ Parsing ------------------ #
    def parse_equation(self, equation_str):
        """
        Parsea una ecuación diferencial en formato string
        Formatos: dy/dx = f(x,y), y' = ..., y'' = ..., M dx + N dy = 0
        """
        equation_str = equation_str.replace(" ", "")
        equation_str = equation_str.replace("^", "**")
        equation_str = equation_str.replace("y''", "Derivative(y(x), x, 2)")
        equation_str = equation_str.replace("d2y/dx2", "Derivative(y(x), x, 2)")
        equation_str = equation_str.replace("dy/dx", "Derivative(y(x), x)")
        equation_str = equation_str.replace("y'", "Derivative(y(x), x)")

        placeholder = "__YFUNC__"
        equation_str = equation_str.replace("y(x)", placeholder)
        equation_str = re.sub(r"y(?!\()", "y(x)", equation_str)
        equation_str = equation_str.replace(placeholder, "y(x)")
        return equation_str

    def _parse(self, expr, local_dict=None):
        loc = local_dict or self.parse_locals
        return parse_expr(expr, local_dict=loc, transformations=self.transformations)

    def _prepare_ics(self, initial_conditions):
        if not initial_conditions:
            return None
        x0 = initial_conditions.get("x0") if isinstance(initial_conditions, dict) else None
        y0 = initial_conditions.get("y0") if isinstance(initial_conditions, dict) else None
        yp0 = initial_conditions.get("yp0") if isinstance(initial_conditions, dict) else None
        ypp0 = initial_conditions.get("ypp0") if isinstance(initial_conditions, dict) else None
        if not any([y0, yp0, ypp0]):
            return None
        if x0 is None:
            raise ValueError("Debe especificar x0 para aplicar condiciones iniciales")
        try:
            x0 = sp.sympify(x0)
            ics = {}
            if y0 is not None:
                ics[self.y(self.x).subs(self.x, x0)] = sp.sympify(y0)
            if yp0 is not None:
                ics[diff(self.y(self.x), self.x).subs(self.x, x0)] = sp.sympify(yp0)
            if ypp0 is not None:
                ics[diff(self.y(self.x), self.x, 2).subs(self.x, x0)] = sp.sympify(ypp0)
            return ics or None
        except (sp.SympifyError, ValueError) as exc:
            raise ValueError(f"Condiciones iniciales inválidas: {exc}")

    def _dsolve(self, eq, y, initial_conditions=None):
        ics = self._prepare_ics(initial_conditions)
        return dsolve(eq, y, ics=ics) if ics else dsolve(eq, y)

    # ------------------ Métodos de resolución ------------------ #
    def solve_separable(self, equation_str, initial_conditions=None):
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            if "=" in eq_str:
                lhs, rhs = eq_str.split("=")
                eq = Eq(self._parse(lhs), self._parse(rhs))
            else:
                eq = self._parse(eq_str)

            special_solution = self._solve_special_cases(eq)
            if special_solution:
                return special_solution
            solution = self._dsolve(eq, y, initial_conditions)
            if isinstance(solution, list):
                solution = solution[0]
            return self._ok(solution, "Variables Separables")
        except Exception as e:
            return self._fail(e, "Variables Separables")

    def solve_homogeneous(self, equation_str, initial_conditions=None):
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            if "=" in eq_str:
                lhs, rhs = eq_str.split("=")
                eq = Eq(self._parse(lhs), self._parse(rhs))
            else:
                eq = self._parse(eq_str)

            special_solution = self._solve_special_cases(eq)
            if special_solution:
                return special_solution
            solution = self._dsolve(eq, y, initial_conditions)
            if isinstance(solution, list):
                solution = solution[0]
            return self._ok(simplify(solution), "Ecuación Homogénea")
        except Exception as e:
            return self._fail(e, "Ecuación Homogénea")

    def solve_exact(self, M_str, N_str):
        try:
            x, y = self.x, symbols("y")
            local_symbols = {
                "x": x,
                "y": y,
                "E": sp.E,
                "e": sp.E,
                "pi": sp.pi,
                "PI": sp.pi,
                "exp": sp.exp,
            }
            M = self._parse(M_str, local_dict=local_symbols)
            N = self._parse(N_str, local_dict=local_symbols)
            dM_dy = diff(M, y)
            dN_dx = diff(N, x)
            is_exact = simplify(dM_dy - dN_dx) == 0
            if is_exact:
                F = integrate(M, x)
                g_y = integrate(N - diff(F, y), y)
                F = F + g_y
                solution_eq = Eq(sp.simplify(F), Symbol("C"))
                return self._ok(solution_eq, "Ecuación Exacta", extra={"is_exact": True})
            else:
                return {
                    "success": False,
                    "error": f"No es exacta. ∂M/∂y={dM_dy}, ∂N/∂x={dN_dx}",
                    "method": "Ecuación Exacta",
                    "is_exact": False,
                }
        except Exception as e:
            return self._fail(e, "Ecuación Exacta")

    def solve_linear(self, equation_str, initial_conditions=None):
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            if "=" in eq_str:
                lhs, rhs = eq_str.split("=")
                eq = Eq(self._parse(lhs), self._parse(rhs))
            else:
                eq = self._parse(eq_str)
            solution = self._dsolve(eq, y, initial_conditions)
            if isinstance(solution, list):
                solution = solution[0]
            return self._ok(solution, "Ecuación Lineal")
        except Exception as e:
            return self._fail(e, "Ecuación Lineal")

    def solve_bernoulli(self, equation_str, initial_conditions=None):
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            if "=" in eq_str:
                lhs, rhs = eq_str.split("=")
                eq = Eq(self._parse(lhs), self._parse(rhs))
            else:
                eq = self._parse(eq_str)
            solution = self._dsolve(eq, y, initial_conditions)
            if isinstance(solution, list):
                solution = solution[0]
            return self._ok(solution, "Ecuación de Bernoulli")
        except Exception as e:
            return self._fail(e, "Ecuación de Bernoulli")

    def find_integrating_factor(self, M_str, N_str):
        try:
            x, y = self.x, symbols("y")
            local_dict = {
                "x": x,
                "y": y,
                "E": sp.E,
                "e": sp.E,
                "pi": sp.pi,
                "PI": sp.pi,
                "exp": sp.exp,
            }
            M = self._parse(M_str, local_dict=local_dict)
            N = self._parse(N_str, local_dict=local_dict)
            dM_dy = diff(M, y)
            dN_dx = diff(N, x)

            try:
                factor_x = (dM_dy - dN_dx) / N
                factor_x_simplified = simplify(factor_x)
                if not factor_x_simplified.has(y):
                    mu = exp(integrate(factor_x_simplified, x))
                    return self._ok(mu, "Factor Integrante μ(x)", extra={"type": "mu(x)"})
            except Exception:
                pass

            try:
                factor_y = (dN_dx - dM_dy) / M
                factor_y_simplified = simplify(factor_y)
                if not factor_y_simplified.has(x):
                    mu = exp(integrate(factor_y_simplified, y))
                    return self._ok(mu, "Factor Integrante μ(y)", extra={"type": "mu(y)"})
            except Exception:
                pass

            return {"success": False, "error": "No se encontró un factor integrante simple", "method": "Factor Integrante"}
        except Exception as e:
            return self._fail(e, "Factor Integrante")

    def solve_general(self, equation_str, initial_conditions=None):
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            if "=" in eq_str:
                lhs, rhs = eq_str.split("=")
                eq = Eq(self._parse(lhs), self._parse(rhs))
            else:
                eq = self._parse(eq_str)
            special_solution = self._solve_special_cases(eq)
            if special_solution:
                return special_solution
            solution = self._dsolve(eq, y, initial_conditions)
            hints = sp.classify_ode(eq, y)
            return self._ok(solution, "Método General", extra={"hints": hints})
        except Exception as e:
            return self._fail(e, "Método General")

    def solve_second_order_constant_coeff(self, equation_str, initial_conditions=None):
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            if "=" in eq_str:
                lhs, rhs = eq_str.split("=")
                eq = Eq(self._parse(lhs), self._parse(rhs))
            else:
                eq = self._parse(eq_str)
            solution = dsolve(eq, y, ics=self._prepare_ics(initial_conditions))
            hints = sp.classify_ode(eq, y)
            is_homogeneous = "nth_linear_constant_coeff_homogeneous" in hints
            return self._ok(
                solution,
                "Segundo Orden Coef. Constantes",
                extra={"is_homogeneous": is_homogeneous},
            )
        except Exception as e:
            return self._fail(e, "Segundo Orden Coef. Constantes")

    def solve_reducible_to_first_order(self, equation_str, case_type="general", initial_conditions=None):
        try:
            y = self.y(self.x)
            eq_str = self.parse_equation(equation_str)
            if "=" in eq_str:
                lhs, rhs = eq_str.split("=")
                eq = Eq(self._parse(lhs), self._parse(rhs))
            else:
                eq = self._parse(eq_str)
            solution = dsolve(eq, y, ics=self._prepare_ics(initial_conditions))
            return self._ok(solution, "Ecuación Reducible a Primer Orden")
        except Exception as e:
            return self._fail(e, "Ecuación Reducible a Primer Orden")

    # ------------------ Casos especiales ------------------ #
    def _solve_special_cases(self, eq):
        handlers = (self._solve_case_y_times_ypp_plus_yp_sq,)
        for handler in handlers:
            result = handler(eq)
            if result:
                return result
        return None

    def _solve_case_y_times_ypp_plus_yp_sq(self, eq):
        y = self.y(self.x)
        expr = sp.simplify(eq.lhs - eq.rhs) if isinstance(eq, sp.Equality) else sp.simplify(eq)
        target = sp.simplify(sp.diff(y * diff(y, self.x), self.x))
        if sp.simplify(expr - target) == 0:
            solution_eq = Eq(y**2, self.C1 * self.x + self.C2)
            return self._ok(solution_eq, "Caso especial: y*y'' + (y')^2 = 0")
        return None

    # ------------------ Helpers de salida ------------------ #
    def _ok(self, solution, method, extra=None):
        return {
            "success": True,
            "solution": str(solution),
            "solution_formatted": self.format_solution(solution),
            "solution_latex": self.get_latex_solution(solution),
            "method": method,
            **(extra or {}),
        }

    def _fail(self, exc, method):
        return {
            "success": False,
            "error": str(exc),
            "method": method,
        }


# Instancia reutilizable
advanced_solver = ODESolver()
