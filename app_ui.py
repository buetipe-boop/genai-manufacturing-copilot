import json
import streamlit as st
from google.genai.errors import ClientError

from app.agent import run_agent


# ---------- Demo outputs (no API calls) ----------
DEMO_OUTPUTS = {
    "Troubleshooting": {
        "summary": "The conveyor motor trips after ~15 minutes with current spikes and heat smell, suggesting increased mechanical load after the recent bearing replacement.",
        "probable_causes": [
            {
                "cause": "Improper bearing installation (preload/fit/seating)",
                "confidence": 0.9,
                "why": "Issue started immediately after bearing batch change; poor seating or preload increases friction and load."
            },
            {
                "cause": "Motor-to-shaft misalignment introduced during maintenance",
                "confidence": 0.75,
                "why": "Reassembly after bearing change can disturb alignment, increasing radial/axial loads and current draw."
            },
            {
                "cause": "Insufficient/incorrect lubrication",
                "confidence": 0.6,
                "why": "Wrong grease type/quantity can cause rapid heat build-up and overload trips."
            }
        ],
        "diagnostic_steps": [
            "Apply Lockout/Tagout (LOTO) before inspection.",
            "Inspect bearing housings for discoloration, grease purge, debris, or abnormal wear.",
            "Measure bearing housing temperature with an IR thermometer after a short controlled run (if safe).",
            "Check coupling/shaft alignment (straight edge or laser tool).",
            "Decouple motor and run unloaded briefly to isolate motor vs. driven equipment.",
            "Measure current draw and compare to nameplate / baseline values."
        ],
        "actions": {
            "immediate": [
                "Stop conveyor and allow components to cool before inspection.",
                "Verify correct bearing part number and installation procedure used.",
                "Check lubrication spec and re-lube if out of spec (per SOP)."
            ],
            "long_term": [
                "Introduce alignment verification step in maintenance checklist.",
                "Implement periodic vibration/thermal checks for critical conveyors.",
                "Review supplier batch QC if multiple bearings show early failure signs."
            ]
        },
        "risks_and_safety": [
            "Electrical shock risk: ensure power isolation and verify zero energy state.",
            "Hot surfaces risk after trip event.",
            "Unexpected restart risk: use LOTO and confirm interlocks before re-energizing."
        ],
        "assumptions": [
            "Motor ran normally before the bearing replacement.",
            "Trip is overload protection rather than a short-circuit fault.",
            "Bearings replaced are in the drive train affecting motor load."
        ]
    },
    "Process Documentation": {
        "sop_title": "Operating Procedure: Press Start-Up and Monitoring",
        "purpose": "Ensure safe, consistent press start-up and operation with defined checks and stop conditions.",
        "required_tools_ppe": [
            "Safety glasses",
            "Cut-resistant gloves (as applicable)",
            "Hearing protection",
            "IR thermometer (optional for verification)",
            "Batch/shift log sheet"
        ],
        "steps": [
            {
                "step_no": 1,
                "instruction": "Put on required PPE and confirm area is clear of obstructions.",
                "critical_point": "Do not operate without PPE; ensure guards are in place."
            },
            {
                "step_no": 2,
                "instruction": "Power on the press and set temperature to 180°C.",
                "critical_point": "Confirm temperature setting matches product spec before start."
            },
            {
                "step_no": 3,
                "instruction": "Wait 5 minutes for stabilization; verify temperature and pressure gauges are within range.",
                "critical_point": "If temperature/pressure deviates, stop and notify supervisor."
            },
            {
                "step_no": 4,
                "instruction": "Start operation and monitor for abnormal noise or vibration.",
                "critical_point": "Any abnormal noise → stop immediately and apply LOTO before inspection."
            },
            {
                "step_no": 5,
                "instruction": "Record batch number, temperature, and pressure reading in the log.",
                "critical_point": "Accurate logging is required for traceability."
            }
        ],
        "checklist": [
            "PPE worn",
            "Guards in place",
            "Temperature set to 180°C",
            "Stabilization wait completed (5 min)",
            "Pressure gauge within range",
            "Batch number recorded"
        ],
        "stop_conditions": [
            "Abnormal noise/vibration",
            "Temperature or pressure out of specification",
            "Guard/interlock malfunction",
            "Visible material jam or debris in operation zone"
        ],
        "common_mistakes": [
            "Skipping stabilization time",
            "Not recording batch/shift info",
            "Continuing operation despite abnormal noise",
            "Incorrect temperature setting vs. product spec"
        ]
    },
    "Defect Report": {
        "executive_summary": "Defects are concentrated in Scratch (~63%) and Misalignment (~27%). The spike coincides with a new operator on Shift B and a supplier batch change, requiring immediate containment and root-cause validation.",
        "top_defects": [
            {"defect": "Scratch", "share_estimate": "63%", "note": "Dominant contributor; likely handling/fixture/contact issue."},
            {"defect": "Misalignment", "share_estimate": "27%", "note": "Possible fixture drift or setup variation."},
            {"defect": "Crack", "share_estimate": "10%", "note": "Lower frequency; verify material brittleness and process stress points."}
        ],
        "likely_causes": [
            "Handling/transfer contact points not controlled (Scratch)",
            "Fixture positioning drift or incorrect setup (Misalignment)",
            "Material variation from new supplier batch",
            "Training gap for new operator on Shift B"
        ],
        "containment_actions": [
            "Increase inspection frequency on Shift B for 48 hours",
            "Add temporary protective film or contact-point padding where scratches occur",
            "Quarantine and label new supplier batch; run controlled comparison lot",
            "Assign an experienced operator to shadow Shift B for one shift"
        ],
        "recommended_experiments": [
            "A/B test: old vs. new supplier batch under identical settings",
            "Fixture repeatability check and re-calibration; measure alignment before/after run",
            "Operator method study: compare handling steps vs. standard work",
            "Short DOE: contact pressure / transfer speed vs. scratch rate (if applicable)"
        ],
        "data_gaps": [
            "No baseline defect trend before supplier change (need last 2–4 weeks)",
            "No measurement of fixture wear or alignment over time",
            "No machine vibration/temperature logs around defect spikes"
        ]
    }
}


def _example_input(label: str) -> str:
    examples = {
        "Troubleshooting": """Line: Conveyor motor
Issue: Motor trips after 15 minutes, current spikes, smell of heat.
Recent change: new bearing batch installed yesterday.
Goal: identify likely causes and next diagnostic steps.""",
        "Process Documentation": """Notes:
Wear PPE. Start press. Set temp 180C. Wait 5 minutes.
If abnormal noise, stop. Record batch number and pressure reading.
Make this a clean SOP with checklist and stop conditions.""",
        "Defect Report": """Defect counts (last 3 shifts):
Scratch: 42
Misalignment: 18
Crack: 7
Context: New operator on Shift B, supplier batch changed.
Generate a short defect analysis report."""
    }
    return examples[label]


# ---------- Streamlit UI ----------
st.set_page_config(page_title="GenAI Manufacturing Copilot", layout="wide")
st.title("GenAI Manufacturing Copilot (Gemini)")

mode_label = st.selectbox(
    "Choose agent mode",
    ["Troubleshooting", "Process Documentation", "Defect Report"]
)

mode_map = {
    "Troubleshooting": "troubleshoot",
    "Process Documentation": "process_doc",
    "Defect Report": "defect_report",
}

# Keep Demo mode ON by default to avoid quota issues
demo_mode = st.toggle("Use Demo Mode (no API calls)", value=True)

st.subheader("Input")
user_input = st.text_area(" ", value=_example_input(mode_label), height=170)

run_clicked = st.button("Run")

if run_clicked:
    try:
        if demo_mode:
            result_obj = DEMO_OUTPUTS[mode_label]
        else:
            with st.spinner("Calling Gemini..."):
                raw = run_agent(mode_map[mode_label], user_input)
            # raw should be JSON text; parse to display as structured JSON
            result_obj = json.loads(raw)

        st.subheader("Structured Output")
        st.json(result_obj)

    except ClientError as e:
        # Common: 429 quota exceeded
        st.error("Gemini API error (likely quota/rate limit). Switch on Demo Mode or enable billing.")
        st.exception(e)

    except json.JSONDecodeError:
        st.error("Model output was not valid JSON. (This is exactly what evaluation + prompt tuning fixes.)")
        st.write("Raw output:")
        st.code(raw)

    except Exception as e:
        st.error("Unexpected error.")
        st.exception(e)
