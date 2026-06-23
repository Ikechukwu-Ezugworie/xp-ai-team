import subprocess
import json
import sys

def fetch_runs(repo, limit=50):
    result = subprocess.run(
        ["gh", "run", "list", "--repo", repo, "--limit", str(limit), "--json",
         "databaseId,conclusion,createdAt,updatedAt,name"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

if __name__ == "__main__":
    repo = sys.argv[1]
    runs = fetch_runs(repo)
    passed = sum(1 for r in runs if r["conclusion"] == "success")
    failed = sum(1 for r in runs if r["conclusion"] == "failure")
    print(f"Passed: {passed}, Failed: {failed}, Total: {len(runs)}")