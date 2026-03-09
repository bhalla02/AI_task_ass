import sympy as sp
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

transformations = standard_transformations + (implicit_multiplication_application,)



class SymbolicMathTool:

    @staticmethod
    def verify_derivative(problem_text: str, final_answer: str) -> bool:
        try:
            if "derivative of" in problem_text.lower():
                expr_str = problem_text.lower().split("derivative of")[-1].strip()
            else:
                return False

            # Replace ^ with ** for sympy compatibility
            expr_str = expr_str.replace("^", "**")
            final_answer = final_answer.replace("^", "**")

            x = sp.symbols('x')

            # Parse the expression and compute the derivative
            expr = parse_expr(expr_str, transformations=transformations)
            computed_derivative = sp.diff(expr, x)

            # Parse the model answer
            model_answer = parse_expr(final_answer, transformations=transformations)

            # Simplify and compare
            difference = sp.simplify(sp.expand(computed_derivative - model_answer))

            # Debugging logs (optional, remove in production)
            print(f"Expression: {expr}")
            print(f"Computed Derivative: {computed_derivative}")
            print(f"Model Answer: {model_answer}")
            print(f"Difference: {difference}")

            return difference == 0

        except Exception as e:
            print(f"Verification failed: {e}")
            return False

    @staticmethod
    def verify_quadratic(problem_text: str, final_answer: str) -> bool:
        """
        Verify quadratic equation roots.
        """

        try:
            x = sp.symbols('x')

            # Extract equation
            equation = problem_text.lower().replace("solve", "").strip()

            if "=" not in equation:
                return False

            left, right = equation.split("=")
            expr = sp.sympify(left) - sp.sympify(right)

            # Extract roots from model answer
            roots = [sp.sympify(r.strip()) for r in final_answer.replace("and", ",").split(",")]

            for r in roots:
                if sp.simplify(expr.subs(x, r)) != 0:
                    return False

            return True

        except Exception:
            return False

    @staticmethod
    def verify_determinant(problem_text: str, final_answer: str) -> bool:
        try:
            if "determinant" not in problem_text.lower():
                return False

            # Extract matrix portion
            matrix_str = problem_text.lower().split("determinant of")[-1].strip()

            matrix = sp.Matrix(eval(matrix_str))

            computed = matrix.det()

            model = parse_expr(final_answer, transformations=transformations)

            return sp.simplify(computed - model) == 0

        except Exception:
            return False

    @staticmethod
    def verify_probability(final_answer: str) -> bool:
        try:
            value = float(sp.N(parse_expr(final_answer)))
            return 0 <= value <= 1
        except Exception:
            return False

    @staticmethod
    def verify_equation(problem_text: str, final_answer: str) -> bool:
        try:
            x = sp.symbols('x')

            # Clean equation
            equation = problem_text.lower().replace("solve", "").strip()

            if "=" not in equation:
                return False

            equation = equation.replace("^", "**")
            left, right = equation.split("=")

            expr = parse_expr(left, transformations=transformations) - \
                parse_expr(right, transformations=transformations)

            # -------- FIX START --------
            # Remove variable assignments like "x ="
            cleaned_answer = final_answer.replace("x =", "")
            cleaned_answer = cleaned_answer.replace("=", "")
            cleaned_answer = cleaned_answer.replace("and", ",")
            cleaned_answer = cleaned_answer.strip()

            # Split roots
            solutions = [
                parse_expr(sol.strip(), transformations=transformations)
                for sol in cleaned_answer.split(",")
                if sol.strip()
            ]
            # -------- FIX END --------

            # Verify each solution
            for solution in solutions:
                if sp.simplify(expr.subs(x, solution)) != 0:
                    return False

            return True

        except Exception as e:
            print(f"Equation verification failed: {e}")
            return False