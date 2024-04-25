


# VivaVoce 🎤

VivaVoce is a web application designed to facilitate remote examinations and assessments. It allows teachers to create tests, students to participate in exams, and provides automated evaluation and feedback using google cloud vertex ai utilizing gemini 1.5x model.

## Features

- **Teacher Dashboard**: Teachers can create tests, manage questions, and review student submissions.
- **Student Dashboard**: Students can join exams using a unique code, answer questions, and receive instant feedback.
- **Automated Evaluation**: The application automatically evaluates student responses, providing scores and feedback.
- **Speech-to-Text Integration**: Allows students to answer questions using speech input, which is converted to text for evaluation.
- **Text-to-Speech Integration**: Provides audio feedback for students' answers and exam results.
- **Secure Authentication**: Uses Firebase Authentication for secure user authentication and data management.

## Technologies Used

1. **Vertex AI**: Vertex AI is a managed machine learning (ML) platform provided by Google Cloud. In the application, it's used for generative models for text comparison and feedback generation.

2. **Pyrebase**: Pyrebase is a Python wrapper for the Firebase platform, which provides tools and services for building web and mobile applications.

3. **Google Cloud Speech-to-Text (STT)**: Google Cloud Speech-to-Text is a service that converts speech into text for further processing and analysis.

4. **Streamlit**: Streamlit is a Python library used for building interactive web applications with simple Python scripts.

5. **gTTS (Google Text-to-Speech)**: gTTS is a Python library and CLI tool to interface with Google Translate's text-to-speech API.

These technologies collectively enable various functionalities within the VivaVoce application, such as creating tests, managing questions, evaluating student responses, providing feedback, and handling authentication.

## Installation

1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/vivavoce.git
   ```
2. Install the required dependencies.
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application.
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Teacher Login**: Teachers can log in using their credentials to access the dashboard.
2. **Teacher Dashboard**: Create a new test by providing test name, questions, and correct answers.
3. **Student Login**: Students log in using their credentials or sign up if they are new users.
4. **Student Dashboard**: Enter the examination code provided by the teacher to start the exam.
5. **Answer Questions**: Students can answer questions using text input or speech-to-text.
6. **Submit Answers**: Submit the answers once completed to receive instant feedback and scores.

## Contributors

- [Your Name](https://github.com/yourusername)
- [Collaborator Name](https://github.com/collaboratorusername)

## License

This project is licensed under the [MIT License](LICENSE).
