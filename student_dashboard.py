# student_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")   # Prevent display backend errors

# -----------------------------
# 1. Load the Dataset
# -----------------------------
try:
    df = pd.read_csv("students_data.csv")
except FileNotFoundError:
    st.error("❌ ERROR: 'students_data.csv' file not found. Place it in the same folder.")
    st.stop()

# Clean NaN values
df = df.fillna({
    "Course": "Unknown",
    "City": "Unknown",
    "Gender": "Unknown",
    "Name": "Unknown",
    "Marks": 0,
    "Attendance": 0
})

# Ensure marks & attendance are numeric
if "Marks" in df.columns:
    df["Marks"] = pd.to_numeric(df["Marks"], errors="coerce").fillna(0)

if "Attendance" in df.columns:
    df["Attendance"] = pd.to_numeric(df["Attendance"], errors="coerce").fillna(0)

st.title("🎓 Student Performance Dashboard")

st.header("📊 Overview of Student Data")
st.dataframe(df)

# -----------------------------
# 2. Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filter Students")

# Course filter
courses = df["Course"].unique().tolist() if "Course" in df.columns else []
selected_course = st.sidebar.selectbox("Select Course", ["All"] + courses)

# City filter
cities = df["City"].unique().tolist() if "City" in df.columns else []
selected_cities = st.sidebar.multiselect("Select City", cities, default=cities)

# Marks filter
if "Marks" in df.columns:
    min_marks = int(df["Marks"].min())
    max_marks = int(df["Marks"].max())
    marks_filter = st.sidebar.slider("Minimum Marks", min_marks, max_marks, min_marks)
else:
    marks_filter = 0

# Gender filter
if "Gender" in df.columns:
    gender_option = st.sidebar.radio("Select Gender", ["All", "Male", "Female", "Unknown"])
else:
    gender_option = "All"

# Apply filters
filtered_df = df.copy()

if selected_course != "All":
    filtered_df = filtered_df[filtered_df["Course"] == selected_course]

if selected_cities:
   filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]

filtered_df = filtered_df[filtered_df["Marks"] >= marks_filter]

if gender_option != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_option]

# -----------------------------
# 3. Display Filtered Data
# -----------------------------
st.subheader("🎯 Filtered Student Data")
st.dataframe(filtered_df)

# -----------------------------
# 4. Display Key Metrics
# -----------------------------
if not filtered_df.empty:
    avg_marks = filtered_df["Marks"].mean()
    avg_attendance = filtered_df["Attendance"].mean() if "Attendance" in df.columns else 0
    total_students = len(filtered_df)

    st.metric("Average Marks", f"{avg_marks:.2f}")
    st.metric("Average Attendance", f"{avg_attendance:.2f}%")
    st.metric("Total Students", total_students)

    # Performance message
    if avg_marks > 85:
        st.success("Excellent performance! 🌟")
    elif avg_marks >= 70:
        st.info("Good performance.")
    else:
        st.warning("Needs improvement.")
else:
    st.error("No students match the filters!")

# -----------------------------
# 5. Search by Student Name
# -----------------------------
st.subheader("🔎 Search Student by Name")
name_search = st.text_input("Enter Student Name:")

if name_search and "Name" in df.columns:
    result = df[df["Name"].str.contains(name_search, case=False, na=False)]
    if not result.empty:
        st.write(result)
    else:
        st.warning("No student found with that name.")

# -----------------------------
# 6. Buttons: Top Performers / Show All
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("Show Top Performers (Marks > 90)"):
        if "Marks" in df.columns:
            top_students = df[df["Marks"] > 90]
            st.subheader("🏆 Top Performers")
            st.dataframe(top_students)
        else:
            st.warning("Marks column not available!")

with col2:
    if st.button("Show All Data"):
        st.subheader("📋 All Student Data")
        st.dataframe(df)

# -----------------------------
# 7. Charts
# -----------------------------
st.header("📈 Charts and Visualizations")

# Bar chart - Marks
if "Marks" in df.columns and "Name" in df.columns and not filtered_df.empty:
    st.bar_chart(filtered_df.set_index("Name")["Marks"])

# Line chart - Attendance
if "Attendance" in df.columns and "Name" in df.columns and not filtered_df.empty:
    st.line_chart(filtered_df.set_index("Name")["Attendance"])

# Histogram
if "Marks" in df.columns:
    fig, ax = plt.subplots()
    ax.hist(filtered_df["Marks"], bins=10)
    st.pyplot(fig)

# -----------------------------
# 8. Add Image
# -----------------------------
st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", width=250)
