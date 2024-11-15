import streamlit as st
import pandas as pd
import pg8000.native
import json

# Page configuration
st.set_page_config(page_title="Dashboard", layout="wide")

# Database configuration


@st.cache_data
def get_connection():
    # Parse the service account JSON from secrets
    service_account_info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
    instance_connection_name = "aiceanographers:europe-west3:django-amphitrite"

    # Create the connection with the Cloud SQL instance connection string
    conn = pg8000.native.Connection(
        user=st.secrets["db"]["db_user"],
        password=st.secrets["db"]["db_password"],
        database=st.secrets["db"]["db_database"],
        # Cloud SQL Proxy connection string format
        host=f'/cloudsql/{instance_connection_name}'
    )
    return conn

# Fetch data


@st.cache_data
def fetch_data(query):
    conn = get_connection()
    cursor = conn.run(query)
    data = [dict(row) for row in cursor]
    df = pd.DataFrame(data)
    conn.close()
    return df


# Main app
st.title("Comprehensive Dashboard")

try:
    # Replace 'your_table' with the actual table name
    query = "SELECT * FROM your_table LIMIT 100;"
    data = fetch_data(query)
    st.dataframe(data)

    # Example visualization if data has numeric columns
    if not data.empty:
        st.bar_chart(data.select_dtypes(include='number'))
except Exception as e:
    st.error(f"Error: {e}")
