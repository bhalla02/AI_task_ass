from backend.llm.groq_client import GroqClient


class ExplainerAgent:

    def __init__(self):
        self.llm = GroqClient(temperature=0.3)

    def explain(self, parsed_problem, solver_output):

        system_prompt = """
You are a helpful math tutor.

Your job:
Explain the solution in a clear, step-by-step way for a student.

Rules:
- Do NOT recompute the answer.
- Use the solver's result.
- Explain concepts simply.
- Show steps clearly.
- Avoid unnecessary text.
- Return structured JSON only.

JSON format:

{
 "explanation_steps": [],
 "concepts_used": []
}
"""

        user_prompt = f"""
Problem:
{parsed_problem["problem_text"]}

Solver result:
Final Answer: {solver_output["final_answer"]}

Solver steps:
{solver_output["solution_steps"]}
"""

        result = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            json_mode=True
        )

        return result