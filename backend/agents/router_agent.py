class RouterAgent:
    def __init__(self):
        self.topic_keywords = {
            "calculus": [
                "derivative", "differentiate", "limit",
                "integral", "optimize", "maximum", "minimum"
            ],
            "probability": [
                "probability", "coin", "dice", "bayes",
                "independent", "conditional", "binomial"
            ],
            "linear_algebra": [
                "determinant", "matrix", "inverse",
                "rank", "eigenvalue"
            ],
            "algebra": [
                "equation", "solve", "root",
                "quadratic", "log", "inequality"
            ]
        }

    def route(self, parsed_output: dict) -> dict:
        text = parsed_output["problem_text"].lower()

        for topic, keywords in self.topic_keywords.items():
            for word in keywords:
                if word in text:
                    return {
                        "topic": topic,
                        "confidence": 0.9
                    }

        # fallback to parser guess
        return {
            "topic": parsed_output.get("topic_guess", "algebra"),
            "confidence": 0.6
        }