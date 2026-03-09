from .text_preprocessor import TextPreprocessor
from .image_preprocessor import ImagePreprocessor
from .audio_preprocessor import AudioPreprocessor


class MultimodalInputRouter:

    def __init__(self):

        self.text_processor = TextPreprocessor()
        self.image_processor = ImagePreprocessor()
        self.audio_processor = AudioPreprocessor()

    def process(self, input_type, data):

        if input_type == "text":
            return self.text_processor.process(data)

        if input_type == "image":
            return self.image_processor.process(data)

        if input_type == "audio":
            return self.audio_processor.process(data)

        raise ValueError("Unsupported input type")