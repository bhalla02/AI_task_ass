from backend.llm.groq_client import GroqClient
from backend.rag.retriever import Retriever


class SolverAgent:
    def __init__(self):
        self.llm = GroqClient(temperature=0.2)
        self.retriever = Retriever()

    def solve(self, parsed_output: dict, routed_output: dict) -> dict:
        problem_text = parsed_output["problem_text"]
        topic = routed_output["topic"]

        retrieved_chunks = self.retriever.retrieve(problem_text, score_threshold=0.15)

        context_text = "\n\n".join(
            [chunk["text"] for chunk in retrieved_chunks]
        )

        sources = list(set([chunk["source"] for chunk in retrieved_chunks]))

        system_prompt = """
You are a JSON-only math solver. 

STRICT OUTPUT RULES — violating these will break the application:
- Your ENTIRE response must be a single valid JSON object
- Do NOT write any text before or after the JSON
- Do NOT use markdown (no ##, no **, no bullet points)
- Do NOT use LaTeX (no \\boxed{}, no \\(, no \\), no $...$)
- Do NOT add explanations, headers, or "The final answer is:"
- ALL steps go inside the "solution_steps" array as plain strings

Your response must start with {{ and end with }} — nothing else.

Required JSON format:
{{
  "solution_steps": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "final_answer": "...",
  "confidence_score": 0.95
}}
"""

        user_prompt = f"""Topic: {topic}

Problem: {problem_text}

Retrieved Context: {context_text}

Respond with JSON only. No explanations outside the JSON."""

        result = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            json_mode=True
        )

        result["used_sources"] = sources

        return result