from __future__ import annotations
import os
import json
import csv


def get_version() -> str:
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "VERSION")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip().split("\n")[0]
    except Exception:
        return "v0.0.0-dev"


def load_top100_json(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_submission_csv(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_output_paths(base_dir: str | None = None) -> dict:
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return {
        "submission": os.path.join(base_dir, "outputs", "phase46_submission.csv"),
        "top100_json": os.path.join(base_dir, "outputs", "phase46_top100.json"),
        "report": os.path.join(base_dir, "outputs", "phase46_report.md"),
    }


def outputs_exist(base_dir: str | None = None) -> bool:
    paths = get_output_paths(base_dir)
    return os.path.isfile(paths["submission"]) and os.path.isfile(paths["top100_json"])


def get_pipeline_stats(top100: list[dict]) -> dict:
    scores = [float(r.get("final_score", 0) or 0) for r in top100]
    ri = [float(r.get("retrieval_intelligence", 0) or 0) for r in top100]
    hp = [float(r.get("honeypot_probability", 0) or 0) for r in top100]

    return {
        "count": len(top100),
        "score_min": round(min(scores), 2),
        "score_max": round(max(scores), 2),
        "score_mean": round(sum(scores) / len(scores), 2) if scores else 0,
        "score_spread": round(max(scores) - min(scores), 2),
        "specialist_pct": round(sum(1 for v in ri if v >= 0.3) / len(ri) * 100, 1) if ri else 0,
        "zero_retrieval": sum(1 for v in ri if v == 0),
        "high_honeypot_risk": sum(1 for v in hp if v > 0.8),
    }
