import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# ===============================
# Load Data
# ===============================
csv_data = """
Date,Product,Region,Units Sold,Price per Unit
2024-01-01,A,North,120,10
2024-01-02,B,South,80,20
2024-01-03,A,East,150,10
2024-01-04,C,West,60,25
2024-01-05,B,North,90,20
2024-01-06,C,East,70,25
2024-01-07,A,South,130,10
"""

df = pd.read_csv(StringIO(csv_data))
df["Date"] = pd.to_datetime(df["Date"])
df["Total Sale"] = df["Units Sold"] * df["Price per Unit"]

# ===============================
# Streamlit Layout
# ===============================
st.title("📊 Sales Dashboard")
st.write("This dashboard shows sales insights by Product, Region, and Date.")

# Sidebar Filters
st.sidebar.header("🔍 Filters")
selected_region = st.sidebar.multiselect(
    "Select Region(s):", df["Region"].unique(), default=df["Region"].unique()
)
selected_product = st.sidebar.multiselect(
    "Select Product(s):", df["Product"].unique(), default=df["Product"].unique()
)

# Apply filters
filtered_df = df[(df["Region"].isin(selected_region)) & (df["Product"].isin(selected_product))]

# Show filtered data
st.subheader("📋 Filtered Data")
st.dataframe(filtered_df)

# ===============================
# Charts
# ===============================

# Split layout into 2 columns
col1, col2 = st.columns(2)

# Bar Chart: Sales by Product
with col1:
    st.subheader("💰 Total Sales by Product")
    product_sales = filtered_df.groupby("Product")["Total Sale"].sum()
    fig1, ax1 = plt.subplots()
    product_sales.plot(kind="bar", color="lightgreen", ax=ax1)
    ax1.set_ylabel("Sales ($)")
    st.pyplot(fig1)

# Pie Chart: Sales by Region
with col2:
    st.subheader("🌍 Sales Distribution by Region")
    region_sales = filtered_df.groupby("Region")["Total Sale"].sum()
    fig2, ax2 = plt.subplots()
    region_sales.plot(kind="pie", autopct="%1.1f%%", startangle=90, ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

# Line Chart: Daily Sales Trend
st.subheader("📈 Daily Sales Trend")
daily_sales = filtered_df.groupby("Date")["Total Sale"].sum()
fig3, ax3 = plt.subplots()
daily_sales.plot(marker="o", linestyle="-", color="orange", ax=ax3)
ax3.set_ylabel("Total Sale ($)")
ax3.set_xlabel("Date")
st.pyplot(fig3)

