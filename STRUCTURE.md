# Reliable Multimodal Math Mentor — Project Structure

This project implements a production-grade AI Math Mentor using:
- RAG (Retrieval Augmented Generation)
- Multi-Agent Architecture
- Symbolic Verification (SymPy)
- Human-in-the-Loop (HITL)
- Persistent Memory
- Multimodal Inputs (Text, Image, Audio)

---

#  High-Level Architecture

User Input (Text / Image / Audio)
        ↓
Multimodal Processing Layer
        ↓
Parser Agent
        ↓
Intent Router Agent
        ↓
Memory Retrieval (similar solved problems)
        ↓
RAG Retriever (formulas/templates)
        ↓
Solver Agent (+ SymPy tool)
        ↓
Verifier Agent
        ↓
Explainer Agent
        ↓
Confidence Scoring
        ↓
HITL (if needed)
        ↓
Memory Store