from backend.tools.symbolic_math import SymbolicMathTool


class VerifierAgent:

    def verify(self, parsed_output: dict, routed_output: dict, solver_output: dict) -> dict:

        problem_text = parsed_output["problem_text"]
        topic = routed_output["topic"]
        final_answer = solver_output["final_answer"]

        verified = False
        issues = []

        if topic == "calculus":
            verified = SymbolicMathTool.verify_derivative(problem_text, final_answer)

        elif topic == "algebra":
            verified = SymbolicMathTool.verify_equation(problem_text, final_answer)

        elif topic == "linear_algebra":
            verified = SymbolicMathTool.verify_determinant(problem_text, final_answer)

        elif topic == "probability":
            verified = SymbolicMathTool.verify_probability(final_answer)

        else:
            issues.append("Unsupported topic for verification.")

        confidence = 0.9 if verified else 0.2

        if not verified:
            issues.append("Symbolic verification failed.")

        return {
            "verified": verified,
            "issues": issues,
            "confidence": confidence
        }