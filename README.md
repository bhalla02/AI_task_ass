# 🧠 Reliable Multimodal Math Mentor  
**RAG + Multi-Agent + Human-in-the-Loop + Memory**

An AI-powered math assistant capable of solving **JEE-style math problems** using a reliable architecture built with:

- Retrieval Augmented Generation (RAG)
- Multi-Agent System
- Multimodal Inputs (Text, Image, Audio)
- Symbolic Verification
- Human-in-the-Loop (HITL)
- Memory-based Learning

The system explains solutions step-by-step and improves reliability through verification and feedback.

---

# 🚀 Features

## 1️⃣ Multimodal Input
Users can ask questions via:

- **Text input**
- **Image upload (OCR)**
- **Voice recording (microphone)**

Pipeline:


---

## 2️⃣ Multi-Agent Architecture

The system uses specialized AI agents:

| Agent | Role |
|-----|-----|
| Parser Agent | Cleans and structures the problem |
| Router Agent | Classifies the math topic |
| Solver Agent | Generates solution using RAG |
| Verifier Agent | Symbolically verifies correctness |
| Explainer Agent | Produces student-friendly explanation |

---

## 3️⃣ Retrieval Augmented Generation (RAG)

A curated math knowledge base is embedded and indexed using FAISS.

RAG provides:

- mathematical identities
- solving strategies
- domain constraints
- common mistakes

This reduces hallucinations and improves reasoning accuracy.

---

## 4️⃣ Symbolic Verification

Solutions are verified using **SymPy** to ensure mathematical correctness.

Examples:

- derivative validation
- determinant verification
- equation solving validation
- probability bounds check

---

## 5️⃣ Human-in-the-Loop (HITL)

Human intervention is triggered when:

- OCR confidence is low
- Speech transcription is unclear
- Parser detects ambiguous problems
- Verifier confidence is low

Users can edit the extracted question before solving.

---

## 6️⃣ Memory & Learning

The system stores solved problems and feedback.

Stored information:

- original question
- parsed structure
- retrieved context
- final solution
- verification results
- user feedback

This enables **similar problem retrieval and pattern reuse**.

---

# 🧱 System Architecture

```mermaid
flowchart TD

User[User Input]

User --> Text[Text Input]
User --> Image[Image Input]
User --> Audio[Audio Input]

Image --> OCR[OCR Extraction]
Audio --> ASR[Speech to Text]

OCR --> Parser
ASR --> Parser
Text --> Parser

Parser --> Router
Router --> Memory[Memory Retrieval]
Memory --> RAG

RAG --> Solver
Solver --> Verifier
Verifier --> Explainer

Explainer --> UI[User Interface]

UI --> Feedback
Feedback --> MemoryStore[Memory Storage]



 Installation
git clone https://github.com/yourusername/math-mentor-ai.git
cd math-mentor-ai


Create VM 
python -m venv venv
source venv/bin/activate


---Install dependencies:

pip install -r requirements.txt


▶️ Running the App

Start the Streamlit application:

streamlit run streamlit_app.py



## System Architecture
flowchart TD

%% USER INPUT
U[User]

U --> T[Text Input]
U --> I[Image Upload]
U --> A[Voice Recording]

%% MULTIMODAL PROCESSING
I --> OCR[OCR Extraction]
A --> ASR[Speech-to-Text]

OCR --> CLEAN[Input Normalization]
ASR --> CLEAN
T --> CLEAN

%% PARSER
CLEAN --> P[Parser Agent]

P --> HITL1{Ambiguity?}

HITL1 -- Yes --> HUMAN1[Human Clarification]
HUMAN1 --> P

HITL1 -- No --> R[Router Agent]

%% MEMORY
R --> MEMR[Memory Retrieval]

%% RAG
MEMR --> RETRIEVE[RAG Retriever]
RETRIEVE --> KB[Knowledge Base]

KB --> SOLVER

%% SOLVER
SOLVER[Solver Agent]

SOLVER --> VERIFY[Verifier Agent]

%% VERIFICATION
VERIFY --> HITL2{Low Confidence?}

HITL2 -- Yes --> HUMAN2[Human Review]
HUMAN2 --> SOLVER

HITL2 -- No --> EXPLAIN

%% EXPLAINER
EXPLAIN[Explainer Agent]

EXPLAIN --> UI[Streamlit UI]

%% FEEDBACK
UI --> FEEDBACK[User Feedback]

%% MEMORY STORAGE
FEEDBACK --> MEMSTORE[Memory Storage]
MEMSTORE --> MEMR