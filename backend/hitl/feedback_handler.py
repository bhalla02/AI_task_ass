class FeedbackHandler:

    def __init__(self, memory_store):
        self.memory_store = memory_store

    def handle_feedback(self, problem_text, result, feedback, comment=None):

        """
        Stores user feedback into memory system.
        """

        feedback_data = {
            "problem_text": problem_text,
            "final_answer": result.get("final_answer"),
            "confidence": result.get("confidence"),
            "verified": result.get("verified"),
            "feedback": feedback,
            "comment": comment
        }

        # store feedback using memory system
        self.memory_store.store_solution(
            problem_text=problem_text,
            parsed_problem=result.get("trace", {}).get("parser", {}),
            topic=result.get("trace", {}).get("router", {}).get("topic", "unknown"),
            retrieved_context=result.get("used_sources", []),
            final_answer=result.get("final_answer"),
            solution_steps=result.get("solution_steps", []),
            verified=result.get("verified"),
            confidence=result.get("confidence"),
            feedback=feedback
        )

        return feedback_data