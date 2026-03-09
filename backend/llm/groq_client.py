import os
import json
import time
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

_client = Groq(api_key=GROQ_API_KEY)


class GroqClient:

    def __init__(self, model: str = GROQ_MODEL, temperature: float = 0.2):
        self.model = model
        self.temperature = temperature


    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2048,
        json_mode: bool = False,
        retries: int = 2,
    ):

        for attempt in range(retries + 1):

            try:

                response = _client.chat.completions.create(
                    model=self.model,
                    temperature=self.temperature,
                    max_tokens=max_tokens,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )

                content = response.choices[0].message.content.strip()

                if json_mode:
                    return self._safe_json_parse(content)

                return content

            except Exception as e:

                if attempt < retries:
                    time.sleep(1)
                else:
                    raise e


    def _safe_json_parse(self, text: str):

        text = text.strip()

        # 1️⃣ Remove markdown code blocks
        if "```" in text:
            parts = text.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    try:
                        return json.loads(part)
                    except json.JSONDecodeError:
                        pass

        # 2️⃣ Direct JSON parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 3️⃣ Strip LaTeX \boxed{...} wrapper and unescape \{ \}
        # Handles: $\boxed{\{ ... \}}$ and \boxed{\{ ... \}}
        boxed_match = re.search(r'\$?\\boxed\{(.*)\}\$?', text, re.DOTALL)
        if boxed_match:
            inner = boxed_match.group(1).strip()
            # Unescape LaTeX-escaped braces: \{ -> {  and \} -> }
            inner = inner.replace(r'\{', '{').replace(r'\}', '}')
            try:
                return json.loads(inner)
            except json.JSONDecodeError:
                pass

        # 4️⃣ Unescape any \{ \} in full text and retry
        unescaped = text.replace(r'\{', '{').replace(r'\}', '}')
        try:
            return json.loads(unescaped)
        except json.JSONDecodeError:
            pass

        # 5️⃣ Find JSON block in unescaped text using brace counting
        result = self._extract_json_by_braces_scan(unescaped)
        if result is not None:
            return result

        raise ValueError(f"LLM did not return valid JSON.\nOutput:\n{text}")


    def _extract_json_by_braces_scan(self, text: str):
        """Scan through text trying each { as a potential JSON start."""
        for i, ch in enumerate(text):
            if ch != "{":
                continue
            brace_count = 0
            in_string = False
            escape_next = False
            for j, c in enumerate(text[i:], i):
                if escape_next:
                    escape_next = False
                    continue
                if c == "\\" and in_string:
                    escape_next = True
                    continue
                if c == '"':
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if c == "{":
                    brace_count += 1
                elif c == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        candidate = text[i:j + 1]
                        try:
                            result = json.loads(candidate)
                            if isinstance(result, dict) and result:
                                return result
                        except json.JSONDecodeError:
                            break
        return None