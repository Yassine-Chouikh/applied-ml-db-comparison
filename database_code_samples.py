"""
UCLA Extension (COM SCI-X 450.1) Final Project — Code Samples
Title: PostgreSQL (SQL) vs MongoDB (NoSQL)

Author: Yassine Chouikh

What this file is:
- A student-friendly “show the idea” script (not a production DB setup).
- Includes example schemas + queries you can copy/paste.
- Also includes the same *illustrative* scalability + performance numbers
  used in my visuals so the repo stays consistent.

Important:
- This script does NOT require a database server to run.
- It prints example SQL and MongoDB queries plus a mini comparison recap.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


# These are the SAME style of numbers referenced in my visual analysis.
# They’re illustrative (benchmarks vary by system), but they keep the repo consistent.
DATA_SCALES = ["1GB", "10GB", "100GB", "1TB", "10TB"]
POSTGRES_EFFICIENCY = [100, 92, 80, 60, 45]   # drops more at huge scale (vertical scaling limits)
MONGO_EFFICIENCY = [100, 97, 90, 80, 70]      # holds up better with sharding (horizontal scaling)

QUERY_TYPES = ["Simple reads", "Complex joins", "Aggregation", "Write-heavy", "Distributed reads"]
POSTGRES_QUERY_SCORE = [95, 90, 85, 70, 60]
MONGO_QUERY_SCORE = [98, 40, 70, 95, 90]


@dataclass
class ExampleBlock:
    title: str
    body: str


def print_header(title: str) -> None:
    print("\n" + "=" * 76)
    print(title)
    print("=" * 76)


def print_examples(blocks: List[ExampleBlock]) -> None:
    for b in blocks:
        print(f"\n--- {b.title} ---")
        print(b.body.strip() + "\n")


def print_mini_table(title: str, rows: List[List[str]]) -> None:
    print_header(title)
    # very simple table printing (keeps it beginner-friendly)
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*rows)]
    for r_i, row in enumerate(rows):
        line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(line)
        if r_i == 0:
            print("-" * len(line))


def postgresql_examples() -> List[ExampleBlock]:
    schema = """
-- Example: a tiny relational schema (patients + visits)
CREATE TABLE patients (
  patient_id SERIAL PRIMARY KEY,
  full_name  TEXT NOT NULL,
  dob        DATE,
  sex        TEXT
);

CREATE TABLE visits (
  visit_id   SERIAL PRIMARY KEY,
  patient_id INT REFERENCES patients(patient_id),
  visit_date DATE NOT NULL,
  diagnosis  TEXT,
  systolic   INT,
  diastolic  INT
);

-- Why SQL shines: relationships + constraints keep data consistent.
"""

    query_join = """
-- Example: a JOIN (classic SQL flex)
SELECT
  p.full_name,
  v.visit_date,
  v.diagnosis,
  v.systolic,
  v.diastolic
FROM patients p
JOIN visits v ON p.patient_id = v.patient_id
WHERE v.visit_date >= '2025-01-01'
ORDER BY v.visit_date DESC;
"""

    query_agg = """
-- Example: aggregate stats (analytics / reporting)
SELECT
  diagnosis,
  COUNT(*) AS n_visits,
  AVG(systolic) AS avg_sys
FROM visits
GROUP BY diagnosis
ORDER BY n_visits DESC;
"""

    return [
        ExampleBlock("PostgreSQL schema (structured tables)", schema),
        ExampleBlock("SQL JOIN example (relational superpower)", query_join),
        ExampleBlock("SQL aggregation example", query_agg),
    ]


def mongodb_examples() -> List[ExampleBlock]:
    doc_model = """
// Example: a document model (patients with embedded visits)
// MongoDB lets you store related stuff together if it fits your app.

{
  "_id": "patient_001",
  "full_name": "Jane Doe",
  "dob": "1990-06-12",
  "sex": "F",
  "visits": [
    {"visit_date": "2025-01-15", "diagnosis": "HTN", "bp": {"sys": 140, "dia": 90}},
    {"visit_date": "2025-02-10", "diagnosis": "HTN", "bp": {"sys": 138, "dia": 88}}
  ]
}
"""

    find_query = """
// Simple query: find all patients with ANY HTN visit
db.patients.find(
  {"visits.diagnosis": "HTN"},
  {"full_name": 1, "visits.$": 1}
)
"""

    aggregation = """
// Aggregation pipeline: average systolic by diagnosis
db.patients.aggregate([
  {$unwind: "$visits"},
  {$group: {_id: "$visits.diagnosis", avg_sys: {$avg: "$visits.bp.sys"}, n: {$sum: 1}}},
  {$sort: {n: -1}}
])
"""

    return [
        ExampleBlock("MongoDB document example (flexible JSON-like storage)", doc_model),
        ExampleBlock("MongoDB find query example", find_query),
        ExampleBlock("MongoDB aggregation example", aggregation),
    ]


def comparison_tables() -> None:
    # Scalability table (matches your visual narrative)
    rows_scale = [["Data size", "PostgreSQL efficiency", "MongoDB efficiency"]]
    for s, p, m in zip(DATA_SCALES, POSTGRES_EFFICIENCY, MONGO_EFFICIENCY):
        rows_scale.append([s, f"{p}%", f"{m}%"])
    print_mini_table("Scalability (illustrative) — consistent with portfolio visuals", rows_scale)

    # Query performance table
    rows_query = [["Query type", "PostgreSQL", "MongoDB"]]
    for qt, p, m in zip(QUERY_TYPES, POSTGRES_QUERY_SCORE, MONGO_QUERY_SCORE):
        rows_query.append([qt, f"{p}%", f"{m}%"])
    print_mini_table("Query performance by workload (illustrative)", rows_query)


def student_takeaways() -> None:
    print_header("My takeaways (student version, not a textbook)")

    print("PostgreSQL is my pick when:")
    print("- the data has clear relationships (patients ↔ visits ↔ labs)")
    print("- correctness/consistency matters (ACID, constraints)")
    print("- you need heavy analytics (joins + aggregations)")

    print("\nMongoDB is my pick when:")
    print("- the data shape changes a lot (new fields every week)")
    print("- you’re writing/ingesting a LOT (logs, sensors, high-throughput)")
    print("- horizontal scaling is a core requirement")

    print("\nAnd the real answer is usually: both.")
    print("- SQL for the “core truth” tables")
    print("- NoSQL for flexible / high-write / app-facing stuff")


def main() -> None:
    print_header("Database Comparison — portfolio demo")
    print("Author: Yassine Chouikh")
    print("\nThis script prints examples + mini comparison tables.")
    print("It does NOT connect to any real databases (so it’s safe to run).")

    print_header("PostgreSQL (SQL) examples")
    print_examples(postgresql_examples())

    print_header("MongoDB (NoSQL) examples")
    print_examples(mongodb_examples())

    comparison_tables()
    student_takeaways()

    print("\nDone. If you’re reading this on GitHub: hii <3")


if __name__ == "__main__":
    main()

