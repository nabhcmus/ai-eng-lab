from ai_eng_lab.extract import JobPosting
from scripts.eval_jd import evaluate


def test_evaluate_reports_accuracy_per_field():
    samples = [
        {
            "id": "one",
            "text": "first",
            "expected": {"title": "AI Engineer", "skills": ["Python", "PyTorch"]},
        },
        {
            "id": "two",
            "text": "second",
            "expected": {"title": "ML Engineer", "skills": ["Python"]},
        },
    ]
    outputs = iter(
        [
            JobPosting(title=" ai engineer ", skills=["python", "PYTORCH"]),
            JobPosting(title="Wrong", skills=["Python", "SQL"]),
        ]
    )

    report = evaluate(samples, extractor=lambda _: next(outputs))

    assert report["fields"]["title"] == {"correct": 1, "total": 2, "accuracy": 0.5}
    assert report["fields"]["skills"] == {"correct": 1, "total": 2, "accuracy": 0.5}
