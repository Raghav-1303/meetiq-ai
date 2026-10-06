# 🎙️ MeetIQ AI

## Intelligent Meeting Insights Platform

**MeetIQ AI** is a full-stack AI-powered meeting assistant that transforms meeting recordings and uploaded audio files into clear summaries and actionable tasks.

Instead of manually taking notes during meetings, users can record audio directly from the browser or upload an existing meeting recording. MeetIQ AI processes the audio, converts speech into text, generates a concise meeting summary, and identifies important follow-up actions.

---



## 📸 Application Status

✅ MeetIQ AI is fully functional and running locally.

The application currently supports:
- 🎤 Live meeting recording
- 📤 Audio file upload
- 🗣️ AI speech-to-text transcription
- 🧠 AI meeting summarization
- ✅ Action item generation

---
## 🚀 Live Demo

Experience MeetIQ AI:

🔗 [Try MeetIQ AI](YOUR-PUBLIC-URL)

---

## ✨ Key Features

- 🎤 **Live Voice Recording**  
  Record meetings directly from the browser using the JavaScript `MediaRecorder API`.

- 📤 **Audio File Upload**  
  Upload existing MP3, WAV, or other supported audio files for AI processing.

- 🗣️ **Speech-to-Text**  
  Uses OpenAI's `Whisper-Tiny` model to convert meeting audio into text.

- 🧠 **AI Meeting Summarization**  
  Uses `BART-Large-CNN` to transform meeting transcripts into concise and readable summaries.

- ✅ **Action Item Generation**  
  Analyzes meeting content to identify actionable statements and organize follow-up tasks.

- 📊 **Structured Task Information**  
  Action items can be organized by Task, Owner, Due Date, and Priority.

---

## 📋 Example Action Items

| Task | Owner | Due Date | Priority |
|------|-------|----------|----------|
| Fix API performance issue | John | Friday | High |
| Update documentation | Sarah | Monday | Medium |
| Deploy application release | DevOps Team | Oct 15 | High |

---

## 🏗️ Technical Architecture

MeetIQ AI follows a simple full-stack AI processing workflow:

```text
Meeting Audio
      ↓
Record Audio / Upload File
      ↓
FastAPI Backend
      ↓
Whisper Speech-to-Text
      ↓
Meeting Transcription
      ↓
BART-Large-CNN
      ↓
AI Meeting Summary
      ↓
Action Item Processing
      ↓
Task | Owner | Due Date | Priority
```

---

## 💻 Frontend

The frontend is built using:

- HTML5
- CSS3
- JavaScript
- MediaRecorder API
- Fetch API
- FormData / Multipart File Upload

The browser's `MediaRecorder API` captures microphone audio and converts it into an audio `Blob`.

The audio file is then sent to the FastAPI backend using an HTTP POST request.

---

## ⚙️ Backend

The backend is developed using:

- Python
- FastAPI
- Pydantic
- REST APIs

FastAPI handles:

- Audio file uploads
- Temporary file storage
- Speech-to-text processing
- Meeting summarization
- Action-item processing
- API responses

---

## 🤖 AI / NLP

### OpenAI Whisper

MeetIQ AI uses the `openai/whisper-tiny` model for automatic speech recognition.

```text
Meeting Audio → Whisper → Meeting Transcription
```

---

### BART-Large-CNN

The `facebook/bart-large-cnn` model is used to summarize meeting transcripts.

```text
Meeting Transcription → BART → Meeting Summary
```

---

### Action Item Processing

After the meeting content is processed, MeetIQ AI analyzes action-oriented statements and organizes them into structured information such as:

```text
Task
Owner
Due Date
Priority
```

This makes it easier for users to understand what needs to be completed after a meeting.

---

## 🔄 Application Workflow

```text
User
 ↓
Record Meeting / Upload Audio
 ↓
JavaScript MediaRecorder
 ↓
Multipart Form Data
 ↓
FastAPI
 ↓
Whisper
 ↓
Transcription
 ↓
BART
 ↓
Meeting Summary
 ↓
Action Item Processing
 ↓
Structured Meeting Insights
```

---

## 📦 Project Structure

```text
meetiq-ai/
│
├── main.py
│   └── FastAPI backend and AI processing
│
├── index.html
│   └── MeetIQ AI frontend interface
│
├── requirements.txt
│   └── Python dependencies
│
├── packages.txt
│   └── System-level dependencies such as FFmpeg
│
├── Dockerfile
│   └── Docker container configuration
│
└── README.md
    └── Project documentation
```

---

## 🔌 API Endpoints

### Process Audio

```http
POST /process-audio
```

Accepts a recorded or uploaded audio file.

The endpoint:

1. Temporarily stores the audio file.
2. Sends the audio through Whisper.
3. Generates the transcription.
4. Sends the transcription through BART.
5. Generates the meeting summary.
6. Returns the results to the frontend.

Example response:

```json
{
  "message": "• The team discussed the upcoming application release.\n• API performance improvements were reviewed.",
  "original_text": "Full meeting transcription..."
}
```

---

### Generate Action Items

```http
POST /action-items
```

Analyzes meeting content and identifies actionable statements.

Example request:

```json
{
  "text": "John will fix the API issue by Friday. Sarah needs to update the documentation."
}
```

Example response:

```json
{
  "action_items": [
    {
      "task": "John will fix the API issue by Friday.",
      "owner": "John",
      "due_date": "Friday",
      "priority": "Medium"
    },
    {
      "task": "Sarah needs to update the documentation.",
      "owner": "Sarah",
      "due_date": "Not specified",
      "priority": "Medium"
    }
  ]
}
```

---

## 🛠️ Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- MediaRecorder API
- Fetch API

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### AI / Machine Learning

- OpenAI Whisper
- Hugging Face Transformers
- BART-Large-CNN

### DevOps

- Docker
- FFmpeg
- Uvicorn

---

## ⚙️ How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/meetiq-ai.git
```

---

### 2. Navigate to the Project

```bash
cd meetiq-ai
```

---

### 3. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. Install FFmpeg

Make sure FFmpeg is installed on your computer.

Verify the installation:

```bash
ffmpeg -version
```

---

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 6. Start the FastAPI Server

```bash
uvicorn main:app --reload
```

---

### 7. Open MeetIQ AI

Open the following address in your browser:

```text
http://127.0.0.1:8000
```

---

## 🐳 Docker

MeetIQ AI can also run inside a Docker container.

Build the Docker image:

```bash
docker build -t meetiq-ai .
```

Run the container:

```bash
docker run -p 7860:7860 meetiq-ai
```

Then open:

```text
http://localhost:7860
```

---

## 🔮 Future Enhancements

Future versions of MeetIQ AI can include:

- 👥 Speaker identification
- 🔐 User authentication
- 🗂️ Meeting history
- 🗄️ PostgreSQL database integration
- 🤖 Advanced LLM-based action-item extraction
- 🔍 Meeting transcript search
- 📄 Downloadable meeting reports
- 📧 Email integration
- 📅 Calendar integration
- ⚛️ React or Angular frontend
- ☁️ AWS or Azure cloud deployment

---

## 🎯 Project Goal

The goal of **MeetIQ AI** is to demonstrate how modern full-stack development can be combined with AI/NLP technologies to automate common meeting workflows.

The application combines browser-based audio recording, REST APIs, speech recognition, NLP summarization, action-item processing, and containerized deployment into a single full-stack application.

---

## 👨‍💻 About the Project

**MeetIQ AI – Intelligent Meeting Insights Platform**

Built as a Full-Stack AI project using:

`Python` • `FastAPI` • `JavaScript` • `Whisper` • `BART` • `Hugging Face Transformers` • `Docker` • `FFmpeg`

---

⭐ If you find MeetIQ AI useful, consider giving the repository a star.