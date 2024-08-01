
# MyAnswer 🎤

MyAnswer is a web application designed to facilitate remote examinations and assessments. It allows teachers to create tests, students to participate in exams, and provides automated evaluation and feedback using Google Cloud Vertex AI utilizing the Gemini 1.5x model.

## Features

- **Teacher Dashboard**: Create tests, manage questions, and review student submissions.
- **Student Dashboard**: Join exams using a unique code, answer questions, and receive instant feedback.
- **Automated Evaluation**: Automatically evaluates student responses, providing scores and detailed feedback.
- **Speech-to-Text Integration**: Enables students to answer questions using speech input, which is converted to text for evaluation.
- **Text-to-Speech Integration**: Provides audio feedback for students' answers and exam results.
- **Secure Authentication**: Uses Firebase Authentication for secure user authentication and data management.

## Technologies Used

1. **Vertex AI**: A managed machine learning (ML) platform provided by Google Cloud, used for generative models for text comparison and feedback generation.

2. **Pyrebase**: A Python wrapper for the Firebase platform, providing tools and services for building web and mobile applications.

3. **Google Cloud Speech-to-Text (STT)**: A service that converts speech into text for further processing and analysis.

4. **Streamlit**: A Python library for building interactive web applications with simple Python scripts.

5. **gTTS (Google Text-to-Speech)**: A Python library and CLI tool to interface with Google Translate's text-to-speech API.

## Installation

### Prerequisites

- Basic knowledge of Python and web development.
- A Google Cloud account.
- Installed software: Python 3.12, Docker

### Setting Up Firebase

1. **Create a Firebase Project**: Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.

2. **Firebase Configuration**: Update the `firebaseConfig` dictionary in the app code with your Firebase project credentials:

   ```python
   firebaseConfig = {
       'apiKey': "YOUR_API_KEY",
       'authDomain': "YOUR_AUTH_DOMAIN",
       'projectId': "YOUR_PROJECT_ID",
       'storageBucket': "YOUR_STORAGE_BUCKET",
       'messagingSenderId': "YOUR_MESSAGING_SENDER_ID",
       'appId': "YOUR_APP_ID",
       'measurementId': "YOUR_MEASUREMENT_ID",
       'databaseURL': 'YOUR_DATABASE_URL'
   }
   ```

3. **Initialize Firebase**: Ensure Firebase is initialized in the application code.

### Setting Up Vertex AI SDK

1. **Enable Vertex AI API**: In the [Google Cloud Console](https://console.cloud.google.com/), enable the Vertex AI API for your project.

2. **Install Vertex AI SDK**: Install the Vertex AI SDK on your local machine:
   ```bash
   pip install google-cloud-aiplatform
   ```

3. **Initialize Vertex AI**: Add the initialization code in your application:

   ```python
   import vertexai

   vertexai.init(project="YOUR_PROJECT_ID", location="YOUR_LOCATION")
   ```

### Running Locally

1. **Clone this repository to your local machine**:
   ```bash
   git clone https://github.com/jebinshaju/myanswer.git
   cd myanswer
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

## Deployment

### Dockerizing the Application

1. **Create a Dockerfile**: Add the Dockerfile to the root of your project:

2. **Build the Docker Image**:
   ```bash
   docker build -t myanswer .
   ```

### Deploying on Google Cloud Run

Follow these steps to deploy the application on Google Cloud Run:

1. **Set Up Environment Variables**:
   ```bash
   GCP_PROJECT='your-gcp-project-id'
   GCP_REGION='your-region'
   AR_REPO='myanswer-repo'
   SERVICE_NAME='myanswer'
   ```

2. **Create Artifact Registry**:
   ```bash
   gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker
   ```

3. **Submit Build to Cloud Build**:
   ```bash
   gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"
   ```

4. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy "$SERVICE_NAME" \
      --port=8080 \
      --image="$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" \
      --allow-unauthenticated \
      --region=$GCP_REGION \
      --platform=managed \
      --project=$GCP_PROJECT \
      --set-env-vars=GCP_PROJECT=$GCP_PROJECT,GCP_REGION=$GCP_REGION
   ```

## Usage

1. **Teacher Login**: Teachers can log in using their credentials to access the dashboard.
2. **Teacher Dashboard**: Create a new test by providing the test name, questions, and correct answers.
3. **Student Login**: Students log in using their credentials or sign up if they are new users.
4. **Student Dashboard**: Enter the examination code provided by the teacher to start the exam.
5. **Answer Questions**: Students can answer questions using text input or speech-to-text.
6. **Submit Answers**: Submit the answers once completed to receive instant feedback and scores.

## License

This project is licensed under the [MIT License](LICENSE).
