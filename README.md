# GenAI Manufacturing Copilot (Gemini)

A structured, testable multi-mode AI agent designed for industrial manufacturing use cases.

This project demonstrates how Generative AI can be engineered — not just prompted — to support real-world factory workflows including troubleshooting, SOP generation, and defect analysis with controlled structured outputs and validation.

---

## 🚀 Overview

The system provides three dedicated AI agent modes:

### 1️⃣ Troubleshooting Agent
- Root cause hypothesis generation
- Confidence scoring per cause
- Structured diagnostic steps
- Immediate containment actions
- Long-term corrective actions
- Safety & risk considerations
- Assumption transparency

### 2️⃣ Process Documentation Agent
- Converts unstructured notes into formal SOP
- Adds PPE requirements
- Adds stop / abort conditions
- Generates structured checklist format
- Improves process standardization

### 3️⃣ Defect Analysis Agent
- Executive summary generation
- Defect distribution breakdown
- Likely root cause reasoning
- Containment actions
- Recommended experiments
- Data gap identification

---

## 🏗 Architecture

- **Model**: Gemini (`gemini-2.5-flash`)
- **Backend**: Python
- **UI**: Streamlit
- **Output Format**: Strict structured JSON
- **Validation Layer**: Custom evaluation framework
- **Robustness Features**:
  - Markdown stripping
  - JSON extraction
  - Schema enforcement
  - Multi-run stability checks

The system is designed to produce deterministic, machine-consumable outputs rather than uncontrolled free-text responses.

---

## 🧪 Reliability & Validation

A custom evaluation layer ensures:

- JSON structure compliance
- Required key presence
- Mode-specific schema validation
- Multi-run consistency

### Evaluation Target

- 3 / 3 test cases passing
- Structured output stability verified
- No uncontrolled free-text responses
- Deterministic JSON format enforcement

Run validation (from project root):

```bash
python -m eval.run_eval

##📂 Project Structure

genai-manufacturing-copilot/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── gemini_client.py
│   └── prompts.py
│
├── eval/
│   ├── test_cases.json
│   └── run_eval.py
│
├── docs/
│   └── screenshots/
│
├── app_ui.py
├── run_demo.py
├── requirements.txt
└── README.md


##⚙️ Installation & Setup

1️⃣ Clone repository

git clone https://github.com/buetipe-boop/genai-manufacturing-copilot.git
cd genai-manufacturing-copilot


2️⃣ Create and activate virtual environment

python -m venv .venv
.venv\Scripts\activate

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Add Gemini API Key (Required for live API mode)

GEMINI_API_KEY=your_api_key_here

[You can generate a free API key at:
https://ai.google.dev/]

▶️ Run the Application

streamlit run app_ui.py

🖥 Demo Mode (No API Required)

If API quota is exceeded or you want to present the system without external calls:

	Enable Demo Mode inside the UI

	Structured output will be simulated


📸 Screenshots

docs/screenshots/

👤 Author

Partha Pratim Sutradhar
M.Eng. Technology & Innovation Management
Focus: Industrial AI, Manufacturing Systems, Digital Transformation