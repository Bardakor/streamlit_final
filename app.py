from sqlalchemy import create_engine

# Database credentials
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "your_gcp_host"  # e.g., "35.123.45.67"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "your_database_name"

def connect_to_database():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        connection = engine.connect()
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

import pandas as pd

def fetch_data(query, connection):
    try:
        data = pd.read_sql(query, con=connection)
        return data
    except Exception as e:
        print("Error fetching data:", e)
        return None


import streamlit as st

# Define your app
def main():
    st.title("Comprehensive Maritime Dashboard")
    st.sidebar.header("Dashboard Options")

    # Connect to the database
    connection = connect_to_database()

    if connection is None:
        st.error("Failed to connect to the database.")
        return

    # Fetch data
    st.sidebar.subheader("Choose a Data Type")
    query_type = st.sidebar.selectbox("Data to Display:", ["Overview", "Details"])

    if query_type == "Overview":
        query = "SELECT * FROM your_table LIMIT 10;"  # Replace with your actual query
    elif query_type == "Details":
        query = "SELECT * FROM another_table;"  # Replace with your actual query

    data = fetch_data(query, connection)

    if data is not None:
        st.subheader("Database Results")
        st.write(data)

        # Display chart
        st.subheader("Data Visualization")
        st.bar_chart(data)
    else:
        st.error("Failed to retrieve data.")

if __name__ == "__main__":
    main()
