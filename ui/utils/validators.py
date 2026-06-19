from __future__ import annotations
import os
import json


def validate_txt_file(path: str) -> tuple[bool, str]:
    if not os.path.isfile(path):
        return False, "File not found"
    if not path.lower().endswith(".txt"):
        return False, "Expected .txt file"
    size = os.path.getsize(path)
    if size == 0:
        return False, "File is empty"
    if size > 10 * 1024 * 1024:
        return False, "File exceeds 10MB limit"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if len(content.strip()) < 10:
            return False, "File appears to contain no meaningful text"
    except Exception as e:
        return False, f"Cannot read file: {e}"
    return True, "Valid"


def validate_jsonl_file(path: str) -> tuple[bool, str]:
    if not os.path.isfile(path):
        return False, "File not found"
    valid_exts = (".jsonl", ".jsonl.gz", ".gz")
    if not any(path.lower().endswith(ext) for ext in valid_exts):
        return False, "Expected .jsonl or .jsonl.gz file"
    size = os.path.getsize(path)
    if size == 0:
        return False, "File is empty"
    if size > 600 * 1024 * 1024:
        return False, "File exceeds 600MB limit"
    try:
        if path.endswith(".gz"):
            import gzip
            fh = gzip.open(path, "rt", encoding="utf-8")
        else:
            fh = open(path, "r", encoding="utf-8")
        with fh:
            line = fh.readline()
            if not line.strip():
                return False, "File appears empty"
            json.loads(line)
    except json.JSONDecodeError:
        return False, "File does not contain valid JSONL (first line not valid JSON)"
    except Exception as e:
        return False, f"Cannot read file: {e}"
    return True, "Valid"
