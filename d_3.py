import streamlit as st
import plotly.express as px
import pandas as pd

st.title("📊 Sample SuperStore EDA")

# Load dataset
try:
    df = pd.read_excel("Sample - Superstore.xls")
except FileNotFoundError:
    st.error("File not found! Please upload the correct dataset.")
    st.stop()

col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the min and max date
startDate = df["Order Date"].min()
endDate = df["Order Date"].max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")

# Filters for Region, State, and City
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
state = st.sidebar.multiselect("Pick the State", df["State"].unique())
city = st.sidebar.multiselect("Pick the City", df["City"].unique())

# Apply Filters
filtered_df = df.copy()

if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]
if state:
    filtered_df = filtered_df[filtered_df["State"].isin(state)]
if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]

# Grouped Sales Data for Category
category_df = filtered_df.groupby("Category", as_index=False)["Sales"].sum()

with col1:
    st.subheader("Category-wise Sales")
    fig = px.bar(category_df, x="Category", y="Sales",
                 text=[f"${x:,.2f}" for x in category_df["Sales"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Region-wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

# Data View & Download Options
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("View Category Data"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv")

with cl2:
    with st.expander("View Region Data"):
        region_sales = filtered_df.groupby("Region", as_index=False)["Sales"].sum()
        st.write(region_sales.style.background_gradient(cmap="Oranges"))
        csv = region_sales.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv")

# Time Series Analysis
filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")

st.subheader('📈 Time Series Analysis')
linechart = filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y-%b"))["Sales"].sum().reset_index()

fig2 = px.line(linechart, x="month_year", y="Sales",
               labels={"Sales": "Amount"},
               height=500, width=1000, template="gridon")
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Time Series Data"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data=csv, file_name="TimeSeries.csv", mime="text/csv")

# Segment & Category-wise Sales Pie Charts
chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment-wise Sales')
    fig = px.pie(filtered_df, values="Sales", names="Segment", template="plotly_dark")
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader('Category-wise Sales')
    fig = px.pie(filtered_df, values="Sales", names="Category", template="gridon")
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
