import pandas as pd
import sys

def compute_metrics(csv_path):
    df = pd.read_csv(csv_path)
    total = len(df)
    valid = df["valid_format"].sum()
    ai_yes = (df["ai_used"] == "YES").sum()
    ai_no  = (df["ai_used"] == "NO").sum()
    by_sprint = df.groupby("sprint").size().rename("commits_per_sprint")
    print(f"Total commits : {total}")
    print(f"Valid format  : {valid} ({100*valid/total:.1f}%)")
    print(f"AI:YES        : {ai_yes}")
    print(f"AI:NO         : {ai_no}")
    print("\nCommits per sprint:")
    print(by_sprint.to_string())

if __name__ == "__main__":
    compute_metrics(sys.argv[1])