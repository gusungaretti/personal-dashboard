import pandas as pd

# load csvs
grades = pd.read_csv("course_grades.csv")
times = pd.read_csv("course_times.csv")

# create mapping dictionary to reduce activity columns
mapping = {
    "Lecture": "lecture",
    "Assignment": "assignment",
    "Review": "review",
    "Exam": "assessment",
    "Quiz": "assessment",
    "Presentation": "assessment",
    "Practice": "practice",
    "Tutorial": "tutorial_lab",
    "Lab": "tutorial_lab",
    "Project": "project",
    "Group Project": "project",
    "Meeting": "project",
}

# apply mapping to create clean column
times["activity_clean"] = times["activity"].map(mapping).fillna("Other")

# convert duration to numeric
times["duration"] = (
    pd.to_timedelta(times["duration"]).dt.total_seconds() / 3600
).round(2)

# aggregate by course code, clean activities
agg = (
    times.groupby(["course_code", "activity_clean"], as_index=False)["duration"]
    .sum()
)

# pivot to wide format
wide = agg.pivot(
    index="course_code",
    columns="activity_clean",
    values="duration"
).reset_index()

wide['total_hours'] = wide[wide.columns.difference(['course_code'])].sum(axis=1).round(2)

# merge with grades table
merged = pd.merge(grades, wide, on="course_code", how="left")

# fill NAs with 0 hours
merged = merged.fillna(0)

# make new csv
merged.to_csv("merged_courses.csv", index=False)
