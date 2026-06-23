import subprocess
import csv
import re
import sys
from datetime import datetime

COMMIT_PATTERN = re.compile(
    r"SPRINT(?P<sprint>\d+)-STORY(?P<story>\d+)-\[AI:(?P<ai>YES|NO)\]-(?P<desc>.+)"
)

def extract_commits(repo_path="."):
    result = subprocess.run(
        ["git", "log", "--pretty=format:%H|%ae|%ai|%s", "--no-merges"],
        cwd=repo_path, capture_output=True, text=True
    )
    rows = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) < 4:
            continue
        sha, email, date_str, subject = parts
        m = COMMIT_PATTERN.match(subject)
        rows.append({
            "sha": sha[:7],
            "author": email,
            "date": date_str,
            "sprint": m.group("sprint") if m else None,
            "story": m.group("story") if m else None,
            "ai_used": m.group("ai") if m else "UNKNOWN",
            "description": m.group("desc") if m else subject,
            "valid_format": bool(m),
        })
    return rows

if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 else "."
    rows = extract_commits(repo)
    writer = csv.DictWriter(sys.stdout, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)