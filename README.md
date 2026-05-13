# Multi Task Gen AI

A FastAPI-based Generative AI project that performs multiple AI-powered tasks such as text summarization and other NLP functionalities.

## Features

- Text Summarization
- FastAPI Backend
- REST API Endpoints
- Environment Variable Support
- Modular Python Structure

## Tech Stack

- Python
- FastAPI
- Uvicorn
- OpenAI API
- REST APIs

## Project Structure

```bash
Multi-Task genAi/
│
├── main.py
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── output_summarize.txt
```

## Installation

### Clone Repository

```bash
git clone https://github.com/SimranKaur1605/Multi_Task-Gen_Ai.git
```

### Move into Project Folder

```bash
cd Multi_Task-Gen_Ai
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

#### Windows

```bash
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Project

```bash
python -m uvicorn main:app --reload
```

Server will run at:

```bash
http://127.0.0.1:8000
```

## Environment Variables

Create a `.env` file and add your API keys:

```env
OPENAI_API_KEY=your_api_key
```

## API Testing

You can test APIs using:

- Postman
- Swagger UI

Swagger URL:

```bash
http://127.0.0.1:8000/docs
```

## Author

Simran Kaur
