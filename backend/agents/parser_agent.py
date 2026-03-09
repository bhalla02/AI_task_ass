from backend.llm.groq_client import GroqClient


class ParserAgent:
    def __init__(self):
        self.llm = GroqClient(temperature=0.1)

    def parse(self, user_input: str) -> dict:
        # Preprocess the input to replace '^' with '**' for valid Python syntax
        user_input = user_input.replace('^', '**')

        system_prompt = """
You are a strict mathematical problem parser.

Your job:
- Clean the input.
- Identify variables.
- Guess topic: algebra, calculus, probability, linear_algebra.
- Detect ambiguity.
- Do NOT solve the problem.
- Return ONLY valid JSON.

JSON format:

{
  "problem_text": "...",
  "variables": [],
  "constraints": [],
  "topic": "algebra | calculus | probability | linear_algebra",
  "needs_clarification": false,
  "clarification_reason": null
}

Rules:
- Extract variables (example: x, y).
- Extract constraints (example: x > 0, integer n).
- Topic must be one of:
  algebra, calculus, probability, linear_algebra.
- If equation seems incomplete → clarification required.
- If probability question missing sample space → clarification required.
- If variables appear without definition → clarification required.
- Never solve the problem.
- Output strictly valid JSON.
"""

        user_prompt = f"Problem:\n{user_input}"

        result = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            json_mode=True
        )

         #  Ensure schema safety
        result = self._ensure_schema(result)

        #  Run rule-based validation
        result = self._validate_parse(result)

        return result
    

    def _ensure_schema(self, parsed: dict) -> dict:

        parsed.setdefault("problem_text", "")
        parsed.setdefault("variables", [])
        parsed.setdefault("constraints", [])
        parsed.setdefault("topic", "algebra")
        parsed.setdefault("needs_clarification", False)
        parsed.setdefault("clarification_reason", None)

        return parsed
    

    def _validate_parse(self, parsed: dict) -> dict:

        text = parsed.get("problem_text", "")

        # Detect incomplete equations
        if "=" not in text and "solve" in text.lower():
            parsed["needs_clarification"] = True
            parsed["clarification_reason"] = "Equation may be incomplete."

        # Probability sanity check
        if parsed.get("topic") == "probability" and "probability" in text.lower():
            if "given" not in text.lower() and "out of" not in text.lower():
                parsed["needs_clarification"] = True
                parsed["clarification_reason"] = "Probability question may lack sample space."

        return parsed