class ConfidenceManager:

    def __init__(self):
        # thresholds can be tuned later
        self.ocr_threshold = 0.8
        self.asr_threshold = 0.75
        self.verification_threshold = 0.6

    def check_multimodal_confidence(self, confidence: float) -> bool:
        """
        Returns True if HITL is required for OCR / ASR extraction.
        """
        return confidence < self.ocr_threshold

    def check_verification_confidence(self, confidence: float) -> bool:
        """
        Returns True if HITL should trigger after verification.
        """
        return confidence < self.verification_threshold

    def check_parser_clarification(self, parsed_output: dict) -> bool:
        """
        Checks if parser flagged ambiguity.
        """
        return parsed_output.get("needs_clarification", False)