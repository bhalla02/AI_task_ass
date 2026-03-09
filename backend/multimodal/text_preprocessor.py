import re


class TextPreprocessor:

    def process(self, text: str):

        if not text:
            return {
                "text": "",
                "confidence": 0.0,
                "source": "text",
                "requires_hitl": True
            }

        cleaned = self._clean_text(text)

        return {
            "text": cleaned,
            "confidence": 1.0,
            "source": "text",
            "requires_hitl": False
        }

    def _clean_text(self, text: str):

        text = text.strip()

        text = re.sub(r"\s+", " ", text)

        return text