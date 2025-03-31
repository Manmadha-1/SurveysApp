import streamlit as st
import mysql.connector
import pandas as pd  # Import pandas for DataFrame manipulation

# Function to establish a connection to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="surveyapp-db1.ctwkcywuyqju.us-east-1.rds.amazonaws.com",
        user="admin",
        password="TOP2020%",
        database="surveysApp_db"
    )

# Function to fetch all records from the 'responses' table
def fetch_all_records():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM responses")  # Replace 'responses' with your table name
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Streamlit app
st.title("Show Records from Database")

# Button to fetch and display records
if st.button("Show Records"):
    records = fetch_all_records()
    if records:
        st.success("Records fetched successfully!")
        # Convert records to a DataFrame and display without index
        df = pd.DataFrame(records)
        df_with_index = df.set_index("id")
        st.write(df_with_index, width=1000, height=300)  # Adjust width and height as needed
    else:
        st.warning("No records found or an error occurred.")