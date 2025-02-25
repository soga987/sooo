import streamlit as st
import pandas as pd
import numpy as np

# Sample Data
data = {
    'Employee': [f'Employee {i}' for i in range(1, 21)],
    'Department': ['HR', 'IT', 'Marketing', 'Finance'] * 5,
    'Hours Worked': np.random.randint(30, 50, 20),
    'Tasks Completed': np.random.randint(5, 20, 20)
}
df = pd.DataFrame(data)

# Sidebar Filter
st.sidebar.header("Filters")
department_filter = st.sidebar.selectbox("Select Department", ['All'] + list(df['Department'].unique()))
if department_filter != 'All':
    df = df[df['Department'] == department_filter]

# KPIs
st.title("Employee Productivity Tracker")
st.metric("Average Hours Worked", f"{df['Hours Worked'].mean():.1f} hrs")
st.metric("Total Tasks Completed", df['Tasks Completed'].sum())

# Data Table
st.subheader("Employee Data")
st.dataframe(df)

# Chart
st.subheader("Hours Worked Distribution")
st.line_chart(df.set_index('Employee')['Hours Worked'])  # Fixed line chart issue

