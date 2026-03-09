import os
from groq import Groq
from dotenv import load_dotenv
import re

load_dotenv()


class AudioPreprocessor:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def process(self, audio_path: str):

        with open(audio_path, "rb") as file:

            transcription = self.client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3"
            )

        text = transcription.text

        cleaned = self._normalize_math_phrases(text)

        confidence = self._estimate_confidence(text)

        requires_hitl = confidence < 0.75

        return {
            "text": cleaned,
            "confidence": confidence,
            "source": "audio",
            "requires_hitl": requires_hitl
        }

    def _normalize_math_phrases(self, text):

        text = text.lower()

        replacements = {
            "square root of": "sqrt",
            "raised to": "^",
            "to the power of": "^",
            "divided by": "/",
            "multiplied by": "*",
            "minus": "-",
            "plus": "+",
            "equals": "="
        }

        for phrase, symbol in replacements.items():
            text = text.replace(phrase, symbol)

        text = re.sub(r"\s+", " ", text)

        return text

    def _estimate_confidence(self, text):

        if not text or len(text) < 5:
            return 0.4

        uncertain_tokens = ["...", "[noise]", "[inaudible]"]

        penalty = sum(token in text.lower() for token in uncertain_tokens)

        confidence = 0.9 - (0.1 * penalty)

        return max(0.5, confidence)