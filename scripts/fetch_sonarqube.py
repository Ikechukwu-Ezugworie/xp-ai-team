import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

SONAR_URL   = os.getenv("SONAR_HOST_URL", "http://localhost:9000")
SONAR_TOKEN = os.getenv("SONAR_TOKEN", "")

def fetch_metrics(project_key, metrics="coverage,bugs,code_smells,duplicated_lines_density"):
    url = f"{SONAR_URL}/api/measures/component"
    params = {"component": project_key, "metricKeys": metrics}
    r = requests.get(url, params=params, auth=(SONAR_TOKEN, ""))
    r.raise_for_status()
    data = r.json()
    return {m["metric"]: m["value"] for m in data["component"]["measures"]}

if __name__ == "__main__":
    import sys
    key = sys.argv[1]
    print(json.dumps(fetch_metrics(key), indent=2))