import sqlite3
import json


class MemoryStore:

    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._initialize_schema()

    def _initialize_schema(self):
        """Initialize the database schema from the schema.sql file."""
        with open("backend/memory/schema.sql", "r") as schema_file:
            schema_sql = schema_file.read()
        self.cursor.executescript(schema_sql)
        self.conn.commit()

    def store_solution(
        self,
        problem_text,
        parsed_problem,
        topic,
        retrieved_context,
        final_answer,
        solution_steps,
        verified,
        confidence,
        feedback=None
    ):

        self.cursor.execute(
            """
            INSERT INTO solved_problems
            (problem_text, parsed_problem, topic, retrieved_context,
             final_answer, solution_steps, verified, confidence, feedback)

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                problem_text,
                json.dumps(parsed_problem),
                topic,
                json.dumps(retrieved_context),
                final_answer,
                json.dumps(solution_steps),
                verified,
                confidence,
                feedback
            )
        )

        self.conn.commit()