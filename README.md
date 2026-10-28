# Derivable Judgement: A Statistical Decision-Making Model

A beginner-friendly Python project for the supplied assignment brief. It generates statistical evidence from a synthetic public-health-style dataset and includes hypothesis tests, confidence intervals, charts, covariance, and correlation.

## Project contents
- `data/health_records.csv` — 600 synthetic health records using the fields in the assignment.
- `src/analyze.py` — analysis script.
- `reports/` — generated charts, summary, JSON results, descriptive statistics, and contingency table (created when you run the script).
- `THEORY_NOTES.md` — short conceptual notes for Part A.
- `requirements.txt` — Python dependencies.

## Important data note
The dataset is artificially generated for coursework. It is **not real patient data**, and results must not be used for medical or clinical decisions. Statistical association does not establish causation.

## Requirements
Python 3.9 or newer is recommended.

## Run the project
1. Extract the ZIP folder.
2. Open a terminal/Command Prompt in the `Derivable_Judgement_Project` folder.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run the analysis:

   ```bash
   python src/analyze.py
   ```

5. Open the `reports` folder to review `analysis_summary.txt`, `analysis_results.json`, CSV summaries, and PNG charts.

## Tests included
1. **Chi-square test:** smoking status vs diabetes status.
2. **Welch two-sample t-test:** BMI mean in records with vs without diabetes.
3. **One-way ANOVA:** glucose level across age groups.
4. **Pearson correlation:** age vs BMI, with p-value.
5. **Covariance:** sample covariance between age and BMI.
6. **95% confidence intervals:** means for age, weight, BMI, blood pressure, cholesterol, and glucose.

Each hypothesis test uses α = 0.05. The script reports “Reject H0” when p < 0.05 and “Fail to reject H0” otherwise. A p-value is not the probability that the null hypothesis is true.

## Suggested GitHub upload
Upload this folder's contents to a repository. Keep `README.md`, source code, data, theory notes, and generated reports together. If your instructor requires a PDF theory document or Jupyter Notebook, those can be added as a next step.
