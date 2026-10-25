"""
main.py
Runs the Student Performance Analytics System.
"""

import numpy as np
import pandas as pd
from functions import *

# Show all columns instead of "..."
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


def print_heading(title):
    """Print a clear section heading."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------- Load data ----------
df = load_data("students.csv")

print_heading("1. DATASET OVERVIEW")
print(df.head())
print("\nColumns:", list(df.columns))
print("Number of records:", len(df))
print()
df.info()

# ---------- Process data ----------
df = calculate_total_and_average(df)
df = assign_grades(df)
df = assign_pass_fail(df)

print_heading("2. PROCESSED DATA")
print(df[["Student_ID", "Name", "Total", "Average", "Grade", "Status"]].to_string(index=False))

# ---------- Analysis ----------
print_heading("3. CLASS PERFORMANCE SUMMARY")

best = df.loc[df["Average"].idxmax()]
worst = df.loc[df["Average"].idxmin()]
print(f"Highest average      : {best['Name']} ({best['Average']})")
print(f"Lowest average       : {worst['Name']} ({worst['Average']})")
print(f"Overall class average: {round(float(np.mean(df['Average'])), 2)}")

passed = (df["Status"] == "Pass").sum()
failed = (df["Status"] == "Fail").sum()
print(f"Passed: {passed} | Failed: {failed} | Pass %: {round(passed / len(df) * 100, 2)}%")

print_heading("4. GRADE DISTRIBUTION")
print(df["Grade"].value_counts())

print_heading("5. SUBJECT-WISE ANALYSIS")
subject_table = subject_analysis(df)
print(subject_table.to_string(index=False))
best_subject = subject_table.loc[subject_table["Average"].idxmax()]
print(f"\nBest performing subject: {best_subject['Subject']} ({best_subject['Average']})")

print_heading("6. DEPARTMENT-WISE AVERAGE")
print(department_analysis(df))

print_heading("7. TOP 3 PERFORMERS")
print(top_performers(df, 3)[["Name", "Department", "Average", "Grade"]].to_string(index=False))

print_heading("8. FAILED STUDENTS")
print(df[df["Status"] == "Fail"][["Name", "Average", "Attendance"]].to_string(index=False))

# ---------- Save results ----------
df.to_csv("results.csv", index=False)
print("\nResults saved to results.csv")