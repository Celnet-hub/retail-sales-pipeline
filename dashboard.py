import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# Database Connection & Data Loading
@st.cache_data
def load_data():
    """
    Connects to PostgreSQL and gets the retail_sales table.
    """
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432")
    )
    
    query = "SELECT * FROM retail_sales"
    df = pd.read_sql(query, conn)
    
    conn.close()
    
    # Ensure date column is datetime objects
    df['date'] = pd.to_datetime(df['date'])
    
    return df

try:
    # get data
    df = load_data()

    # Sidebar Filters
    st.sidebar.header("Filter")
    
    # Store Filter
    selected_stores = st.sidebar.multiselect(
        "Select Stores",
        options=df['store'].unique(),
        default=df['store'].unique() # Select all stores by default
    )
    
    # Category Filter
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=df['category'].unique(),
        default=df['category'].unique() # Select all categories by default

    )
    
    # Apply Filters
    df_filtered = df[
        (df['store'].isin(selected_stores)) & 
        (df['category'].isin(selected_categories))
    ]



    ################### Main Dashboard #########################
    st.title("Argos Retail Performance Dashboard")
    st.markdown("---")

    # Top Row: KPIs
    total_revenue = df_filtered['total_amount'].sum()
    total_transactions = df_filtered.shape[0]
    avg_transaction = df_filtered['total_amount'].mean()

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Revenue", f"£{total_revenue:,.2f}")
    with col2:
        st.metric("Total Transactions", f"{total_transactions:,}")
    with col3:
        st.metric("Avg Transaction Value", f"£{avg_transaction:,.2f}")

    st.markdown("---")

    

    # Middle Row: Charts
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Sales by Store")
        # Group data by store for the chart
        store_sales = df_filtered.groupby('store')['total_amount'].sum().sort_values(ascending=False)
        st.bar_chart(store_sales)

    with col_right:
        st.subheader("Sales by Category")
        category_sales = df_filtered.groupby('category')['total_amount'].sum().sort_values(ascending=False)
        st.bar_chart(category_sales)

    # Bottom Row: Timeline
    st.subheader("Revenue Trend Over Time")
    # Resample by Day or Month for a cleaner line chart
    daily_sales = df_filtered.set_index('date').resample('D')['total_amount'].sum()
    st.line_chart(daily_sales)
    
    # Show Raw Data (Optional toggle)
    if st.checkbox("Show Raw Data"):
        st.dataframe(df_filtered)

except Exception as e:
    st.error(f"Error connecting to database: {e}")