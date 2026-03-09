from backend.agents.parser_agent import ParserAgent
from backend.agents.router_agent import RouterAgent
from backend.agents.solver import SolverAgent
from backend.agents.verifier_agent import VerifierAgent

from backend.multimodal.input_router import MultimodalInputRouter
from backend.agents.explainer_agent import ExplainerAgent

from backend.memory.memory_store import MemoryStore
from backend.memory.memory_retriever import MemoryRetriever
from backend.hitl.confidence_manager import ConfidenceManager


class MathMentorOrchestrator:

    def __init__(self):

        # Multimodal router
        self.input_router = MultimodalInputRouter()

        # Agents
        self.parser = ParserAgent()
        self.router = RouterAgent()
        self.solver = SolverAgent()
        self.verifier = VerifierAgent()
        self.explainer = ExplainerAgent()
        self.memory_store = MemoryStore()
        self.memory_retriever = MemoryRetriever()
        self.confidence_manager = ConfidenceManager()

    def run_pipeline(self, input_type: str, input_data) -> dict:

        trace = {}

        # 0️⃣ Multimodal Processing
        processed_input = self.input_router.process(input_type, input_data)
        trace["multimodal"] = processed_input

        # HITL Trigger (Extraction Level)
        if processed_input.get("requires_hitl"):

            return {
                "status": "needs_review",
                "stage": "multimodal_extraction",
                "extracted_text": processed_input["text"],
                "confidence": processed_input["confidence"],
                "trace": trace
            }

        cleaned_text = processed_input["text"]

        # 1️⃣ Parser Agent
        parsed_output = self.parser.parse(cleaned_text)
        trace["parser"] = parsed_output

        if parsed_output.get("needs_clarification"):

            return {
                "status": "needs_clarification",
                "stage": "parser",
                "trace": trace
            }

        # 2️⃣ Router Agent
        routed_output = self.router.route(parsed_output)
        trace["router"] = routed_output

        # Memory retrieval
        similar_problems = self.memory_retriever.retrieve_similar(
            parsed_output["problem_text"]
        )

        trace["memory_matches"] = similar_problems

        # 3️⃣ Solver Agent
        solver_output = self.solver.solve(parsed_output, routed_output)
        trace["solver"] = solver_output

        # 4️⃣ Verifier Agent
        verification_output = self.verifier.verify(
            parsed_output,
            routed_output,
            solver_output
        )

        trace["verifier"] = verification_output

        # 5️⃣ Generate explanation
        explanation_output = self.explainer.explain(
            parsed_output,
            solver_output
        )

        trace["explainer"] = explanation_output

        # HITL Trigger (Verification Level)
        if self.confidence_manager.check_verification_confidence(
                verification_output.get("confidence", 0.5)
        ):

            return {
                "status": "needs_review",
                "stage": "verification",
                "solver_output": solver_output,
                "verification": verification_output,
                "trace": trace
            }

        # 5️⃣ Combine confidence
        final_confidence = (
            solver_output.get("confidence_score", 0.5) * 0.5 +
            verification_output.get("confidence", 0.5) * 0.5
        )

        # 6️⃣ Store successful solution in memory
        self.memory_store.store_solution(

            problem_text=parsed_output["problem_text"],
            parsed_problem=parsed_output,
            topic=parsed_output["topic"],
            retrieved_context=solver_output.get("used_sources", []),

            final_answer=solver_output["final_answer"],
            solution_steps=solver_output["solution_steps"],

            verified=verification_output["verified"],
            confidence=final_confidence
        )

        # Also add to similarity memory
        self.memory_retriever.add_memory(parsed_output["problem_text"])


        return {
            "status": "success",
            "final_answer": solver_output["final_answer"],
            "solution_steps": explanation_output.get(
                "explanation_steps",
                solver_output["solution_steps"]
            ),
            "concepts_used": explanation_output.get("concepts_used", []),
            "verified": verification_output["verified"],
            "confidence": round(final_confidence, 2),
            "used_sources": solver_output.get("used_sources", []),
            "trace": trace
        }

        # return {
        #     "status": "success",
        #     "final_answer": solver_output["final_answer"],
        #     "solution_steps": explanation_output.get("explanation_steps", solver_output["solution_steps"]),
        #     "concepts_used": explanation_output.get("concepts_used", []),
        #     "verified": verification_output["verified"],
        #     "confidence": round(final_confidence, 2),
        #     "used_sources": solver_output.get("used_sources", []),
        #     "trace": trace
        # }