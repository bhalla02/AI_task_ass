import easyocr
import numpy as np


class ImagePreprocessor:

    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def process(self, image_path: str):

        results = self.reader.readtext(image_path, detail=1)

        if not results:
            return {
                "text": "",
                "confidence": 0.0,
                "source": "image",
                "requires_hitl": True
            }

        extracted_text = " ".join([r[1] for r in results])

        confidence = float(np.mean([r[2] for r in results]))

        requires_hitl = confidence < 0.80

        return {
            "text": extracted_text,
            "confidence": confidence,
            "source": "image",
            "requires_hitl": requires_hitl
        }