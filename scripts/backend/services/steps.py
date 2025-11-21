def symbolic_steps(eq_type: str | None, solution_latex: str | None, original_eq: str | None = None) -> list:
    """Genera pasos genéricos según tipo, incluyendo ecuación original y solución final."""
    type_label = eq_type or "diferencial"
    sol = solution_latex or ""
    orig = original_eq or ""
    return [
        {
            "title": "Identificación",
            "description": f"Se reconoce la ecuación como {type_label}.",
            "equation": orig,
        },
        {
            "title": "Resolución con SymPy",
            "description": "Se usa dsolve para obtener la solución general o particular (si hay CI).",
            "equation": orig,
        },
        {
            "title": "Resultado",
            "description": "Solución encontrada.",
            "equation": sol,
        },
    ]


def numeric_steps(method: str, h: float, n: int) -> list:
    """Pasos genéricos para métodos numéricos."""
    name = "Euler" if method.endswith("euler") else "Runge-Kutta 4"
    return [
        {
            "title": f"Método {name}",
            "description": f"Se itera {n} pasos con h={h}.",
            "equation": "",
        }
    ]
