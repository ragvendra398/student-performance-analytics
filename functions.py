"""
functions.py
Reusable functions for the Student Performance Analytics System.
"""

import pandas as pd
import numpy as np

# Subject columns (must match the CSV headers exactly)
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer"]

# Rules
PASS_MARK = 40          # minimum marks required in every subject
MIN_ATTENDANCE = 75     # minimum attendance percentage


def load_data(file_path):
    """Read the CSV file and return a DataFrame."""
    df = pd.read_csv(file_path)
    return df


def calculate_total_and_average(df):
    """Add 'Total' and 'Average' columns using NumPy."""
    marks = df[SUBJECTS].to_numpy()               # convert to NumPy array
    df["Total"] = np.sum(marks, axis=1)           # row-wise sum
    df["Average"] = np.round(np.mean(marks, axis=1), 2)
    return df


def get_grade(average):
    """Return the grade for one average value."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def assign_grades(df):
    """Loop through every average and assign a grade."""
    grades = []
    for avg in df["Average"]:
        grades.append(get_grade(avg))
    df["Grade"] = grades
    return df


def get_status(row):
    """Return 'Pass' or 'Fail' for one student (one row)."""
    marks_ok = (row[SUBJECTS] >= PASS_MARK).all()     # every subject >= 40
    attendance_ok = row["Attendance"] >= MIN_ATTENDANCE  # attendance >= 75

    if marks_ok and attendance_ok:
        return "Pass"
    else:
        return "Fail"


def assign_pass_fail(df):
    """Add a 'Status' column."""
    df["Status"] = df.apply(get_status, axis=1)
    return df


def subject_analysis(df):
    """Return a table with average, highest and lowest marks per subject."""
    results = []
    for subject in SUBJECTS:                       # loop over subjects
        results.append({
            "Subject": subject,
            "Average": round(float(np.mean(df[subject])), 2),
            "Highest": int(np.max(df[subject])),
            "Lowest": int(np.min(df[subject])),
        })
    return pd.DataFrame(results)


def top_performers(df, n=3):
    """Return the top n students by average marks."""
    return df.sort_values("Average", ascending=False).head(n)


def department_analysis(df):
    """Average marks for each department."""
    return df.groupby("Department")["Average"].mean().round(2)