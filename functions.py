# functions.py
#
# To use:
#   from functions import run_trial_analysis
#   run_trial_analysis(trial_id="PHARMA-101")

import random
import datetime


# Sets up the analysis for a clinical trial and calls generate_patient_data
# ------------------------------------------------------------------
def run_trial_analysis(trial_id, n_patients=50):
    print(f"Starting analysis for trial: {trial_id}")

    trial_name = f"Clinical Trial {trial_id}"
    start_date = datetime.date.today()
    analyst    = "Dr. Rivera"
    status     = "in progress"

    results = generate_patient_data(n_patients)
    return results


# Simulates patient data and calls compute_statistics
# ------------------------------------------------------------------
def generate_patient_data(n):
    random.seed(42)

    patient_ids = [f"PT-{i:03d}" for i in range(1, n + 1)]
    ages        = [random.randint(18, 75) for _ in range(n)]
    weights_kg  = [round(random.gauss(75, 15), 1) for _ in range(n)]
    dosages_mg  = [round(w * 0.5, 2) for w in weights_kg]
    sites       = [random.choice(["Boston", "Chicago", "Houston"]) for _ in range(n)]

    patient_data = [
        {
            "id":     patient_ids[i],
            "age":    ages[i],
            "weight": weights_kg[i],
            "dosage": dosages_mg[i],
            "site":   sites[i],
        }
        for i in range(n)
    ]

    return compute_statistics(patient_data)


# Validates data and calls the final report function
# ------------------------------------------------------------------
def compute_statistics(data):
    n_patients   = len(data)
    mean_age     = sum(r["age"] for r in data) / n_patients
    mean_weight  = sum(r["weight"] for r in data) / n_patients
    dosages      = [r["dosage"] for r in data]
    dosage_range = (min(dosages), max(dosages))
    site_counts  = {}
    for r in data:
        site_counts[r["site"]] = site_counts.get(r["site"], 0) + 1

    required_columns = ["id", "age", "weight", "dosage", "site", "response"]
    existing_columns = list(data[0].keys())
    missing_cols     = set(require_columns) - set(existing_columns)  # ← misspelled name

    if missing_cols:
        raise ValueError(
            "Data validation failed. Missing required column(s): "
            + ", ".join(sorted(missing_cols))
        )

    return format_results(data)    # never reached


# Formats and prints the final report
# ------------------------------------------------------------------
def format_results(data):
    report_title = "=== Trial Analysis Report ==="
    n_sites      = len({r["site"] for r in data})
    avg_dosage   = round(sum(r["dosage"] for r in data) / len(data), 2)
    completion   = f"{len(data)} patients processed across {n_sites} sites."

    print(report_title)
    print(completion)
    print(f"Average dosage: {avg_dosage} mg")

    return {
        "n":          len(data),
        "avg_dosage": avg_dosage,
        "n_sites":    n_sites,
    }
