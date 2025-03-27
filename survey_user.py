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
    cursor.execute("CREATE DATABASE IF NOT EXISTS surveys_db")
    cursor.execute("USE surveys_db")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question_id INT NOT NULL,
            question_text TEXT,
            response_text TEXT,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    """)
    conn.close()

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="surveyapp-db1.ctwkcywuyqju.us-east-1.rds.amazonaws.com",
        user="admin",
        password="TOP2020%",
        database="surveys_db"
    )

# User Interface
def user_interface():
    # Default title
    st.title("Survey Response")
    
    # Step 1: User enters survey ID
    survey_id = st.number_input("Enter Survey ID:", min_value=1, step=1)
    if survey_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch survey name
        cursor.execute("SELECT name FROM surveys WHERE id = %s", (survey_id,))
        survey = cursor.fetchone()
        
        if survey:
            # Update the title dynamically with the survey name
            st.subheader(f"Survey: {survey['name']}")
            
            # Fetch survey questions
            cursor.execute("SELECT * FROM questions WHERE survey_id = %s", (survey_id,))
            questions = cursor.fetchall()
            conn.close()
            
            if questions:
                responses = {}
                missing_required = False  # Flag to track missing required responses
                for question in questions:
                    if question["is_required"]:
                        responses[question["id"]] = st.text_input(f"{question['question_text']} (Required)")
                    else:
                        responses[question["id"]] = st.text_input(f"{question['question_text']}")
                
                # Step 3: Save responses
                if st.button("Save Responses"):
                    # Validate required responses
                    for question in questions:
                        if question["is_required"] and not responses[question["id"]].strip():
                            st.warning(f"Please fill in the required question: {question['question_text']}")
                            missing_required = True
                            break
                    
                    if not missing_required:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        for question_id, response in responses.items():
                            # Fetch the question text for the current question ID
                            question_text = next(q["question_text"] for q in questions if q["id"] == question_id)
                            cursor.execute(
                                "INSERT INTO responses (question_id, question_text, response_text) VALUES (%s, %s, %s)",
                                (question_id, question_text, response)
                            )
                        conn.commit()
                        conn.close()
                        st.success("Thank you for taking the survey!")
            else:
                st.error("No questions found for this survey.")
        else:
            st.error("Survey not found.")
            conn.close()

# Main function
def main():
    setup_database()
    user_interface()

if __name__ == "__main__":
    main()