\# GenAI Manufacturing Copilot (Gemini)



A structured, testable multi-mode AI agent designed for manufacturing use cases.



This project demonstrates how Generative AI can be engineered — not just prompted — to support industrial troubleshooting, SOP generation, and defect analysis with structured outputs and validation.



---



\## 🚀 Overview



This application provides three AI agent modes:



1\. \*\*Troubleshooting Agent\*\*

&nbsp;  - Root cause hypothesis generation

&nbsp;  - Confidence scoring

&nbsp;  - Structured diagnostic steps

&nbsp;  - Immediate and long-term actions

&nbsp;  - Safety and assumption analysis



2\. \*\*Process Documentation Agent\*\*

&nbsp;  - Converts unstructured notes into formal SOP

&nbsp;  - Adds PPE requirements

&nbsp;  - Adds stop conditions

&nbsp;  - Creates checklist format



3\. \*\*Defect Analysis Agent\*\*

&nbsp;  - Executive summary

&nbsp;  - Top defect distribution

&nbsp;  - Likely root causes

&nbsp;  - Containment actions

&nbsp;  - Recommended experiments

&nbsp;  - Data gap identification



---



\## 🏗 Architecture



\- \*\*Model\*\*: Gemini (gemini-2.5-flash)

\- \*\*Backend\*\*: Python

\- \*\*UI\*\*: Streamlit

\- \*\*Output Format\*\*: Strict structured JSON

\- \*\*Validation Layer\*\*: Custom evaluation script

\- \*\*Robustness\*\*: Markdown stripping + JSON extraction



---



\## 🧪 Reliability \& Validation



An evaluation script was implemented to test:



\- JSON structure compliance

\- Required key presence

\- Multi-mode consistency



Evaluation Result:





