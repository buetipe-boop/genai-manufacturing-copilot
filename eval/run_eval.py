import json
import re
from app.agent import run_agent


def looks_like_json(text: str) -> bool:
    text = text.strip()
    return text.startswith("{") and text.endswith("}")


def missing_keys(text: str, keys: list[str]) -> list[str]:
    missing = []
    for k in keys:
        pattern = rf'"{re.escape(k)}"\s*:'
        if not re.search(pattern, text):
            missing.append(k)
    return missing


def main():
    with open("eval/test_cases.json", "r", encoding="utf-8") as f:
        cases = json.load(f)

    passed = 0

    for i, c in enumerate(cases, 1):
        print(f"\n=== Case {i}: {c['name']} ===")
        out = run_agent(c["mode"], c["input"])

        if not looks_like_json(out):
            print("FAIL: Output not JSON-like (doesn't start/end with { }).")
            print(out[:400])
            continue

        miss = missing_keys(out, c["must_have_keys"])
        if miss:
            print("FAIL: Missing keys:", miss)
            print(out[:400])
            continue

        print("PASS")
        passed += 1

    print(f"\nResult: {passed}/{len(cases)} passed")


if __name__ == "__main__":
    main()
