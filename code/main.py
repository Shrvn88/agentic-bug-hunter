import csv
from agent_core.auditor import AuditorOrchestrator

INPUT_FILE = "data/samples.csv"
OUTPUT_FILE = "data/final_report.csv"

def main():

    auditor = AuditorOrchestrator()
    results = []

    with open(INPUT_FILE, newline="", encoding="utf8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            reports = auditor.analyze(row["ID"], row["Code"])

            for r in reports:
                results.append({
                    "ID": r.id,
                    "bug_line": r.bug_line,
                    "Explanation": r.explanation
                })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "bug_line", "Explanation"])
        writer.writeheader()
        writer.writerows(results)

    print("DONE. Saved", len(results), "bugs.")

if __name__ == "__main__":
    main()
