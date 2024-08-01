import streamlit as st
import pyrebase
from vertexai.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold
import uuid,vertexai
import pyperclip
import json
from streamlit_mic_recorder import mic_recorder,speech_to_text
from gtts import gTTS
from tempfile import TemporaryFile
import base64


firebaseConfig = {
   
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

vertexai.init(project="viva-voce-420906", location="asia-south1")
model = GenerativeModel("gemini-1.5-pro-preview-0409")

state=st.session_state



generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}


safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


def teacher_login():
    st.title("Teacher Login")
    email = st.text_input("Email")
    password = st.text_input("password", type="password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state["user"] = user  # Store user data in session state
            teacher_dashboard(user)  # Go to teacher dashboard
        except Exception as e:
            st.error("Invalid credentials. Please try again.")

def write_test_to_database(user,test_name, num_questions, question_inputs, answer_inputs):
    st.title("Questions uploaded sucessfully.")
    test_id = str(uuid.uuid4())[:5]
    test_data = {
        "test_name": test_name,
        "num_questions": num_questions,
        "unique_id": test_id,
        "questions": []
    }

    for i in range(num_questions):
        question = question_inputs[i]
        answer = answer_inputs[i]
        question_data = {
            "question": question,
            "correct_answer": answer,
            "test_id": test_id
        }
        test_data["questions"].append(question_data)

    try:
        db.child("tests").child(test_id).set(test_data)
        st.success(f"Test created with ID: {test_id}")
        pyperclip.copy(test_id)
        st.success("Test ID copied to clipboard")
        db.child("teachers").child(user['localId']).child("tests_created").push(test_id)
    except Exception as e:
        st.error(f"An error occurred: {e}")



def teacher_dashboard(user):
    st.title("Teacher Dashboard")
    st.write(f"Welcome, {user['email']}!")

    st.subheader("Create Test")
    test_name = st.text_input("Test Name")
    num_questions = st.number_input("Number of Questions", min_value=1, max_value=100, step=1)

    questions = []  # List to store input fields for questions
    answers = []    # List to store input fields for answers

    
    with st.form("create_test_form"):
        for i in range(num_questions):
            question = st.text_input(f"Question {i+1}")
            answer = st.text_area(f"Answer for Question {i+1}")
            questions.append(question)
            answers.append(answer)

        submit_button = st.form_submit_button("Create Test")

    if submit_button:
        write_test_to_database(user,test_name, num_questions, questions, answers)

def handle_exam(exam_code,user):
    # Retrieve test data based on the exam code
    test_data = db.child("tests").child(exam_code).get().val()
    questions = test_data.get("questions", [])
    #st.write(test_data["questions"])
    # li = test_data["questions"]

    if test_data:
        st.success("Examination started successfully!")
        st.write("Answer the following questions:")

        # Dictionary to store student answers
        student_answers = {}

        with st.form("answer_form"):
            total_marks = 0 
            for i, question_data in enumerate(questions):
                question_text = question_data['question']
                correct_answer = question_data["correct_answer"]
                
                st.write(f"Question {i+1}: {question_text}")
                try:
                        tts = gTTS(f"Question {i+1}: {question_text}", slow=False)
                        tts.save("audio.mp3")

                        # Read the audio file and convert it to base64
                        with open("audio.mp3", "rb") as audio_file:
                            audio_bytes = base64.b64encode(audio_file.read()).decode("utf-8")

                        # Embed the audio player in HTML format with autoplay
                        audio_html = f'<audio src="data:audio/mp3;base64,{audio_bytes}" autoplay controls>'
                        st.write(f"Question {i+1}: {question_text}")
                        st.write(audio_html, unsafe_allow_html=True)
                except:
                    st.write(":smile:")
                state.text_received=[]
                c1,c2=st.columns(2)
                with c1:
                    text = st.text_area(f"Your Answer for Question {i+1}")
                with c2:
                    text=speech_to_text(language='en',use_container_width=True,just_once=True,key=f'STT{i}')
                    if text:
                        state.text_received.append(text)

                    for text in state.text_received:
                        st.write(text)

                student_answers[question_text] = (text, correct_answer)
                #st.write(text)
                #student_answer = st.text_area(f"Your Answer for Question {i+1}")
                #student_answers[question_text] = (student_answer, correct_answer)

            if st.form_submit_button("Submit Answers"):
                #st.write("djdjfdnfdhnf")
                st.write("Answers submitted successfully!")
                # Print the student's answers
                st.write("RESULTS:")
                for question, answers in student_answers.items():
                    student_answer, correct_answer = answers
                    # student_answer  = student_answer.lower()
                    # correct_answer = correct_answer.lower()
                    st.write(f"Question: {question}\n\nYour Answer: {student_answer}\nCorrect Answer: {correct_answer}")     
                    text1 = f"""Compare both text1(answer provided by teacher) = ({correct_answer}) and text2(answer provided by the student) = ({student_answer}) for the question ({question}) and return whether the two answers are equal, compare them, rate the level of closeness in percentage, and give the difference between these answers like a friendly teacher explaining to a student. Also, convert the results into respective audio files and return all these in a JSON format with the necessary details along with the text and audio. Avoid markup syntax, don't include comments in the file output, also never mention test1 and test2 in response. The JSON should be of this format only: {{
  "comparison_result": {{
    "equality": false,
    "closeness_percentage": 0,
    "difference_explanation": "The first answer, 'Italy,' is incorrect because it is a country, not the capital of France. The second answer, 'Itally,' is also incorrect and seems to be a misspelling of 'Italy.' The correct answer to the question 'What is the capital of France?' is Paris.",
    "audio_explanation": "comparison_explanation.wav"
  }},
  "text1_details": {{
    "text": "Italy",
    "audio": "italy.wav"
  }},
  "text2_details": {{
    "text": "Itally",
    "audio": "itally.wav"
  }}
}}"""

                    responses = model.generate_content(
                        [text1],
                        generation_config=generation_config,
                        safety_settings=safety_settings,
                        stream=True,
                    )

                    # Process responses and create JSON output
                    full_text = ""
                    #output_json = process_responses(responses, teacher_answer, student_answer)
                    for response in responses:
                        #print(response.text, end="")
                        full_text += response.text


                    speech_text = ""
                    
                    full_text=full_text.strip().lstrip("```json").rstrip("```")
                    #st.write(full_text)
                    st.write(f"Correct answer: {correct_answer}")
                    st.write(f"Students answer: {student_answer}")
                    parsed_json = json.loads(full_text)
                    #st.write(parsed_json)
                    st.write(f"Equality: {parsed_json['comparison_result']['equality']}")
                    st.write(f"Closeness Percentage: {parsed_json['comparison_result']['closeness_percentage']}")
                    st.write(f"Explanation: {parsed_json['comparison_result']['difference_explanation']}")
                    closeness_percentage = parsed_json['comparison_result']['closeness_percentage']
                    speech_text += f"Equality: {parsed_json['comparison_result']['equality']}\n"
                    speech_text += f"Closeness Percentage: {parsed_json['comparison_result']['closeness_percentage']}\n"
                    speech_text += f"Explanation: {parsed_json['comparison_result']['difference_explanation']}\n\n"

                    marks = closeness_percentage / 100  # Assuming total marks is scaled to 1
                    total_marks += marks

                    # Display marks for the question
                    st.title(f"Marks Obtained: {marks}")
                    speech_text += f"Marks Obtained: {marks}\n"
                    db.child("students").child(user['localId']).child("tests_taken").child(exam_code).set(f"Explanation: {parsed_json['comparison_result']['difference_explanation']}")
                    #st.write(full_text)
                    try:
                        tts = gTTS(speech_text, slow=False)
                        tts.save("audio.mp3")

                        # Read the generated audio file and convert it to base64
                        with open("audio.mp3", "rb") as audio_file:
                            audio_bytes = base64.b64encode(audio_file.read()).decode("utf-8")

                        # Embed the audio player in HTML format with autoplay
                        audio_html = f'<audio src="data:audio/mp3;base64,{audio_bytes}" autoplay controls>'
                        st.write(audio_html, unsafe_allow_html=True)
                    except:
                        st.write(":smile:")
                st.title(f"Total Marks: {total_marks}")
                try:
                        tts = gTTS(f"Total Marks: {total_marks}",slow = False)
                        tts.save("audio.mp3")
                        file = "./audio.mp3"
                        st.audio(file, format='audio/mp3')
                except:
                    st.write(":smile:")
                db.child("students").child(user['localId']).child("tests_taken").child(exam_code).set({"Total_marks_obtained": total_marks})
            # Handle submission logic here
            # You can access student_answers dictionary here to get the submitted answers

    else:
        st.error("Invalid examination code. Please try again.")


def student_dashboard(user):
    
    try:
        st.title("Student Dashboard")
        st.write("Welcome to the Student Dashboard!")

        st.subheader("Enter Examination Code")
        exam_code = st.text_input("Enter the examination code:")
        st.button("Start/Restart Examination", on_click=handle_exam(exam_code,user))  
    except Exception as e:
        st.write(e)

def teacher_signup():
    st.title("Teacher Signup")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    name = st.text_input("Name")
    if st.button("Signup"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            db.child("teachers").child(user['localId']).set({"email": email, "name": name})
            st.success("Signup successful!")
            st.session_state["user"] = user 
            teacher_dashboard(user)
        except Exception as e:
            st.error(f"Error signing up: {e}")

def student_signup():
    st.title("Student Signup")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    name = st.text_input("Name")
    if st.button("Signup"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            db.child("students").child(user['localId']).set({"email": email, "name": name})
            st.success("Signup successful!")
            st.session_state["user"] = user 
            student_dashboard(st.session_state["user"])
        except Exception as e:
            st.error(f"Error signing up: {e}",)    

def main():
    st.sidebar.title("Navigation")
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <h1 style="color: yellow; font-size: 3em;">VivaVoce <span style="font-size: 1.5em;">🎤</span></h1>
        </div>
        """,
        unsafe_allow_html=True
)
    st.write("VivaVoce is a web application designed to facilitate remote examinations and assessments.")
    st.write("It allows teachers to create tests, manage questions, and review student submissions.")
    st.write("Students can participate in exams, answer questions, and receive instant feedback.")
    
    page = st.sidebar.radio("", ["Teacher Login", "Student Login","Teacher Signup","Student Signup"])
    if page == "Teacher Login" and "user" not in st.session_state:
        st.sidebar.title("Teacher Login")
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user_data = db.child("teachers").child(user['localId']).get()
                if user_data.val() is not None:
                    st.session_state["user"] = user
                    teacher_dashboard(user)
                else:
                    st.sidebar.error("Invalid credentials. Please try again.")
            except Exception as e:
                st.sidebar.error("Invalid credentials. Please try again.")

    elif page == "Student Login" and "user" not in st.session_state:
        st.sidebar.title("Student Login")
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user_data = db.child("students").child(user['localId']).get()
                if user_data.val() is not None:
                    st.session_state["user"] = user
                    student_dashboard(user)
                else:
                    st.sidebar.error("Invalid credentials. Please try again.")
            except Exception as e:
                st.error("Invalid credentials. Please try again.")


    elif page == "Teacher Login" and "user" in st.session_state:
        teacher_dashboard(st.session_state["user"])

    elif page == "Student Login" and "user" in st.session_state:
        student_dashboard(st.session_state["user"])    
    #     ... (implement student login logic) ...
    elif page == "Student Signup":
        student_signup()
    elif page == "Teacher Signup":
        teacher_signup()

    st.sidebar.markdown("---")
    st.sidebar.title("Sign Out")
    if st.sidebar.button("Sign Out"):
        try:
            del st.session_state["user"]  # Remove user from session state
            st.sidebar.success("You have been signed out.")
            
        except Exception as e:
            st.sidebar.error("User not logged in.")
if __name__ == "__main__":
    main()
