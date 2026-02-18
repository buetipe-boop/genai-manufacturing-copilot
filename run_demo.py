from app.agent import run_agent

if __name__ == "__main__":
    sample_input = """Line: Conveyor motor
Issue: Motor trips after 15 minutes, current spikes, smell of heat.
Recent change: new bearing batch installed yesterday.
Goal: identify likely causes and next diagnostic steps.
"""

    out = run_agent("troubleshoot", sample_input)
    print(out)
