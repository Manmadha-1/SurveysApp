import streamlit as st
import mysql.connector

# Database setup
def setup_database():
    conn = mysql.connector.connect(
        host="surveyapp-db1.ctwkcywuyqju.us-east-1.rds.amazonaws.com",
        user="admin",
        password="TOP2020%"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS surveysApp_db")
    cursor.execute("USE surveysApp_db")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS surveys (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question_text VARCHAR(500) NOT NULL,
            is_required BOOLEAN NOT NULL,
            UNIQUE (question_text) -- Ensure unique questions
        )
    """)
    conn.close()

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="surveyapp-db1.ctwkcywuyqju.us-east-1.rds.amazonaws.com",
        user="admin",
        password="TOP2020%",
        database="surveysApp_db"
    )

# Admin Management Console
def admin_console():
    st.title("Admin Management Console")
    
    # Step 1: Create a new survey
    survey_name = st.text_input("Enter Survey Name (Required):")
    survey_created = False  # Flag to track if a survey is created
    if st.button("Create Survey"):
        if survey_name:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO surveys (name) VALUES (%s)", (survey_name,))
            conn.commit()
            conn.close()
            st.success(f"Survey '{survey_name}' created successfully!")
            survey_created = True  # Set the flag to True
        else:
            st.error("Survey name cannot be empty.")
    
    # Step 2: Display question input fields only if a survey is created
    if survey_created or survey_name:  # Check if a survey is created or exists
        st.subheader("Add Questions to the Survey")
        questions = []
        for i in range(1, 5):
            question_text = st.text_input(f"Enter Question {i}:")
            is_required = st.checkbox(f"Is Question {i} required?", key=f"required_{i}")
            questions.append((question_text, is_required))
        
        if st.button("Add Questions"):
            # Filter out empty questions
            valid_questions = [q for q in questions if q[0]]
            
            if len(valid_questions) > 0:  # Ensure at least one question is filled
                conn = get_db_connection()
                cursor = conn.cursor()
                for question_text, is_required in valid_questions:
                    # Check if the question already exists
                    cursor.execute(
                        "SELECT id FROM questions WHERE question_text = %s",
                        (question_text,)
                    )
                    existing_question = cursor.fetchone()
                    
                    if existing_question:
                        st.warning(f"The question '{question_text}' already exists. No duplicate created.")
                    else:
                        # Insert the new question if it doesn't exist
                        cursor.execute(
                            "INSERT INTO questions (question_text, is_required) VALUES (%s, %s)",
                            (question_text, is_required)
                        )
                conn.commit()
                conn.close()
                st.success("Questions added successfully!")
            else:
                st.error("At least one question must be filled.")

    # Step 3: Publish survey
    if st.button("Publish Survey"):
        if survey_name:
            st.success(f"Survey '{survey_name}' published successfully!")
        else:
            st.error("Survey name is required to publish the survey.")

# Main function
def main():
    setup_database()
    admin_console()

if __name__ == "__main__":
    main()