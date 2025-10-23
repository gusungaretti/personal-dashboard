import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load cleaned data
courses = pd.read_csv("merged_courses.csv")

courses2 = courses.drop(columns=['final_grade', 'total_hours'])

sem_courses = courses2.groupby('semester_code').sum(numeric_only=True)

st.bar_chart(sem_courses)