"""Derivable Judgement: Statistical Decision-Making Model
Run from the project root: python src/analyze.py
All records are synthetic and are intended for educational use only.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "health_records.csv"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)
ALPHA = 0.05

df = pd.read_csv(DATA)
for col in ["diabetes", "hypertension"]:
    if df[col].dtype == object:
        df[col] = df[col].astype(str).str.lower().map({"true": True, "false": False})

def decision(p):
    return "Reject H0" if p < ALPHA else "Fail to reject H0"

def ci_mean(series, confidence=0.95):
    x = pd.Series(series).dropna().astype(float)
    mean = x.mean()
    sem = stats.sem(x)
    lo, hi = stats.t.interval(confidence, len(x)-1, loc=mean, scale=sem)
    return {"n": int(len(x)), "mean": float(mean), "lower": float(lo), "upper": float(hi)}

def save_bar(counts, title, xlabel, ylabel, filename):
    ax = counts.plot(kind="bar", rot=0)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(REPORTS / filename, dpi=150)
    plt.close()

results = {
    "dataset": {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "note": "Synthetic educational dataset; not real patient data."
    },
    "confidence_intervals_95": {
        col: ci_mean(df[col]) for col in ["age", "weight", "bmi", "blood_pressure", "cholesterol_level", "glucose_level"]
    },
    "hypothesis_tests": []
}

# Test 1: Smoking status vs diabetes (chi-square test of independence)
cont = pd.crosstab(df["smoking_status"], df["diabetes"])
chi2, p, dof, expected = stats.chi2_contingency(cont)
results["hypothesis_tests"].append({
    "name": "Smoking status vs diabetes (Chi-square test)",
    "H0": "Smoking status and diabetes status are independent in this sample.",
    "H1": "Smoking status and diabetes status are associated in this sample.",
    "test_statistic": float(chi2), "degrees_of_freedom": int(dof), "p_value": float(p),
    "alpha": ALPHA, "decision": decision(p),
    "interpretation": "Evidence of an association at the 5% level." if p < ALPHA else "Insufficient evidence of an association at the 5% level.",
    "contingency_table": cont.to_dict()
})
save_bar(df.groupby("smoking_status", observed=False)["diabetes"].mean()*100,
         "Diabetes prevalence by smoking status", "Smoking status", "Diabetes prevalence (%)",
         "diabetes_by_smoking.png")

# Test 2: BMI comparison by diabetes status (Welch's independent t-test)
yes = df.loc[df["diabetes"] == True, "bmi"].dropna()
no = df.loc[df["diabetes"] == False, "bmi"].dropna()
t_stat, p = stats.ttest_ind(yes, no, equal_var=False)
results["hypothesis_tests"].append({
    "name": "BMI by diabetes status (Welch two-sample t-test)",
    "H0": "Mean BMI is equal for records with and without diabetes.",
    "H1": "Mean BMI differs between records with and without diabetes.",
    "mean_diabetes": float(yes.mean()), "mean_no_diabetes": float(no.mean()),
    "test_statistic": float(t_stat), "p_value": float(p), "alpha": ALPHA,
    "decision": decision(p),
    "interpretation": "Mean BMI differs significantly at the 5% level." if p < ALPHA else "Insufficient evidence of a mean BMI difference at the 5% level."
})

# Test 3: ANOVA of glucose across age groups
groups = [g["glucose_level"].dropna().values for _, g in df.groupby("age_group", observed=True)]
f_stat, p = stats.f_oneway(*groups)
results["hypothesis_tests"].append({
    "name": "Glucose level across age groups (one-way ANOVA)",
    "H0": "Mean glucose level is equal across all age groups.",
    "H1": "At least one age group has a different mean glucose level.",
    "test_statistic": float(f_stat), "p_value": float(p), "alpha": ALPHA,
    "decision": decision(p),
    "interpretation": "At least one age-group mean differs significantly at the 5% level." if p < ALPHA else "Insufficient evidence that mean glucose differs across age groups at the 5% level."
})
save_bar(df.groupby("age_group", observed=True)["glucose_level"].mean(),
         "Mean glucose level by age group", "Age group", "Mean glucose level",
         "mean_glucose_by_age_group.png")

# Test 4: Pearson correlation between age and BMI
r, p = stats.pearsonr(df["age"], df["bmi"])
results["correlation"] = {
    "variables": ["age", "bmi"], "pearson_r": float(r), "p_value": float(p),
    "interpretation": ("Positive" if r > 0 else "Negative" if r < 0 else "No linear") +
                      f" linear correlation; p-value {'is below' if p < ALPHA else 'is not below'} 0.05."
}
results["covariance"] = {
    "age_bmi_sample_covariance": float(df[["age", "bmi"]].cov().iloc[0,1])
}
plt.scatter(df["age"], df["bmi"], alpha=0.55)
plt.title("Age vs BMI")
plt.xlabel("Age (years)")
plt.ylabel("BMI")
plt.tight_layout()
plt.savefig(REPORTS / "age_vs_bmi.png", dpi=150)
plt.close()

# Descriptive statistics and data-quality summary
df.describe(include="all").transpose().to_csv(REPORTS / "descriptive_statistics.csv")
pd.crosstab(df["smoking_status"], df["diabetes"]).to_csv(REPORTS / "smoking_diabetes_contingency.csv")
with open(REPORTS / "analysis_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

# Readable text summary
lines = [
    "DERIVABLE JUDGEMENT — ANALYSIS SUMMARY",
    "=" * 42,
    f"Rows analyzed: {len(df)}",
    f"Significance level: {ALPHA}",
    "Dataset: synthetic, for educational use only.",
    "",
    "95% confidence intervals for means:"
]
for col, val in results["confidence_intervals_95"].items():
    lines.append(f"- {col}: mean={val['mean']:.2f}; 95% CI [{val['lower']:.2f}, {val['upper']:.2f}]")
lines += ["", "Hypothesis tests:"]
for item in results["hypothesis_tests"]:
    lines.append(f"- {item['name']}: statistic={item['test_statistic']:.4f}, p={item['p_value']:.5f}; {item['decision']}.")
    lines.append(f"  {item['interpretation']}")
lines += [
    "",
    f"Pearson correlation (age vs BMI): r={r:.4f}, p={results['correlation']['p_value']:.5f}",
    f"Sample covariance (age vs BMI): {results['covariance']['age_bmi_sample_covariance']:.4f}",
    "",
    "Reminder: statistical association does not establish causation. Do not use synthetic results for clinical decisions."
]
(REPORTS / "analysis_summary.txt").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\nSaved reports and charts in: {REPORTS}")
