from google.genai import types
import re

from .gemini_client import get_gemini_client
from .prompts import (
    TROUBLESHOOT_PROMPT,
    PROCESS_DOC_PROMPT,
    DEFECT_REPORT_PROMPT,
)

MODEL_NAME = "gemini-2.5-flash"


def run_agent(mode: str, user_input: str) -> str:
    """
    Runs one of the manufacturing agents based on mode.
    Returns the model output (expected to be JSON text).
    """

    prompt_map = {
        "troubleshoot": TROUBLESHOOT_PROMPT,
        "process_doc": PROCESS_DOC_PROMPT,
        "defect_report": DEFECT_REPORT_PROMPT,
    }

    if mode not in prompt_map:
        raise ValueError(f"Unknown mode: {mode}. Use one of: {list(prompt_map.keys())}")

    prompt = prompt_map[mode].format(user_input=user_input)

    client = get_gemini_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,  # low randomness = more consistent JSON
        ),
    )

   
    raw = (response.text or "").strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\s*```$", "", raw)
    match = re.search(r"\{[\s\S]*\}", raw)

# Remove Markdown code block if present
    if match:
        return match.group(0).strip()

    return raw


