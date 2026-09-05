import json
from pathlib import Path

from gemini_service import decide_incident
from models import IncidentPayload


TEST_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "test_incidents.json"
)


def load_test_incidents():
    with TEST_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data["incidents"]


def run_tests():
    incidents = load_test_incidents()

    passed = 0
    failed = 0

    for index, test_case in enumerate(incidents, start=1):
        incident = IncidentPayload(
            incident_sys_id=f"test-{index}",
            number=f"TEST{index:03}",
            short_description=test_case["short_description"],
            description=test_case["description"],
            priority=3,
        )

        expected = test_case["expected_decision"]

        try:
            result = decide_incident(incident)
            actual = result.decision

            if actual == expected:
                passed += 1
                status = "PASS"
            else:
                failed += 1
                status = "FAIL"

            print(f"\nTest {index}: {status}")
            print(f"Short description: {incident.short_description}")
            print(f"Expected: {expected}")
            print(f"Actual:   {actual}")
            print(f"Message:  {result.message}")

        except Exception as exc:
            failed += 1

            print(f"\nTest {index}: ERROR")
            print(f"Short description: {incident.short_description}")
            print(f"Expected: {expected}")
            print(f"Error: {exc}")

    print("\n----------------------------")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("----------------------------")

    if failed > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    run_tests()