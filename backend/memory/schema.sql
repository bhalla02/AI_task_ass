CREATE TABLE IF NOT EXISTS solved_problems (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    problem_text TEXT,
    parsed_problem TEXT,

    topic TEXT,

    retrieved_context TEXT,

    final_answer TEXT,
    solution_steps TEXT,

    verified BOOLEAN,
    confidence REAL,

    feedback TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);