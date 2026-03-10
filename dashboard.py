import streamlit as st
import pandas as pd
import plotly.express as px
from database import engine

# Page Configuration
st.set_page_config(page_title="LeadFlow Analytics", layout="wide")

st.title("📊 Lead Research Dashboard")
st.markdown("Real-time insights into sourced leads and data quality.")

# 1. Load Data from Database
def load_data():
    df = pd.read_sql("SELECT * FROM leads", engine)
    return df

df = load_data()

# 2. Key Metrics (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Leads Sourced", len(df))
with col2:
    verified_count = len(df[df['email'].notnull()])
    st.metric("Verified Emails", verified_count)
with col3:
    precision = (verified_count / len(df) * 100) if len(df) > 0 else 0
    st.metric("Verification Rate", f"{precision:.1f}%")

st.divider()

# 3. Visualizations
left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("Leads by Category")
    fig_cat = px.pie(df, names='status', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_cat, use_container_width=True)

with right_chart:
    st.subheader("Lead Acquisition by Company")
    company_counts = df['company'].value_counts().reset_index()
    company_counts.columns = ['Company', 'Count']
    fig_bar = px.bar(company_counts, x='Company', y='Count', color='Count')
    st.plotly_chart(fig_bar, use_container_width=True)

# 4. Raw Data Table
st.subheader("📋 Detailed Lead Database")
st.dataframe(df, use_container_width=True)

# 5. Export Button
st.download_button(
    label="Download Database as CSV",
    data=df.to_csv(index=False),
    file_name="lead_export.csv",
    mime="text/csv"
)