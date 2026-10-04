"""Evaluate JobPosting extraction against the hand-labeled JD sample set."""

import argparse
import json
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from ai_eng_lab.extract import JobPosting, extract

DEFAULT_DATA = Path(__file__).parents[1] / "tests" / "data" / "jd_samples.json"


def _normalize(value: str) -> str:
    return " ".join(value.casefold().split())


def _skills_match(actual: Sequence[str], expected: Sequence[str]) -> bool:
    return {_normalize(skill) for skill in actual} == {
        _normalize(skill) for skill in expected
    }


def evaluate(
    samples: Sequence[dict[str, Any]],
    extractor: Callable[[str], JobPosting] = lambda text: extract(text, JobPosting),
) -> dict[str, Any]:
    """Return exact-match accuracy for title and the complete skills set."""
    field_results = {
        "title": {"correct": 0, "total": len(samples)},
        "skills": {"correct": 0, "total": len(samples)},
    }
    sample_results = []

    for sample in samples:
        expected = sample["expected"]
        error = None
        try:
            actual = extractor(sample["text"])
            title_correct = _normalize(actual.title) == _normalize(expected["title"])
            skills_correct = _skills_match(actual.skills, expected["skills"])
            if title_correct:
                field_results["title"]["correct"] += 1
            if skills_correct:
                field_results["skills"]["correct"] += 1
            actual_values = {
                "title": actual.title,
                "skills": actual.skills,
            }
        except ValueError as exc:
            title_correct = False
            skills_correct = False
            actual_values = None
            error = str(exc)

        sample_results.append(
            {
                "id": sample["id"],
                "title_correct": title_correct,
                "skills_correct": skills_correct,
                "actual": actual_values,
                "error": error,
            }
        )

    for result in field_results.values():
        result["accuracy"] = (
            result["correct"] / result["total"] if result["total"] else 0.0
        )
    return {"fields": field_results, "samples": sample_results}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    args = parser.parse_args()

    with args.data.open(encoding="utf-8") as file:
        samples = json.load(file)
    report = evaluate(samples)
    print(json.dumps(report, ensure_ascii=False, indent=2))

    failed = [
        result
        for result in report["samples"]
        if not result["title_correct"] or not result["skills_correct"]
    ]
    if failed:
        print(
            f"{len(failed)}/{len(samples)} mẫu có ít nhất một trường sai.",
            file=sys.stderr,
        )
        for result in failed:
            wrong_fields = [
                field for field in ("title", "skills") if not result[f"{field}_correct"]
            ]
            detail = f" ({result['error']})" if result["error"] else ""
            print(
                f"- {result['id']}: sai {', '.join(wrong_fields)}{detail}",
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
