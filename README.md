# LinguaAI — Language Translation Tool

A web-based language translation tool built for the **CodeAlpha Artificial Intelligence Internship — Task 1**.

## Features

- Source and target language selection
- Translation through the Google Cloud Translation API
- Clean responsive web interface
- Copy translation button
- Swap source and target languages
- Character counter
- Error handling for missing input and API failures

## Technologies

- Python
- Flask
- HTML
- CSS
- JavaScript
- Google Cloud Translation API

## Project Structure

```text
CodeAlpha_Language_Translation_Tool/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Setup

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the translation API

Create a `.env` file in the project folder:

```text
GOOGLE_TRANSLATE_API_KEY=YOUR_API_KEY
```

Enable the Google Cloud Translation API for the Google Cloud project associated with the key.

### 4. Load environment variables

Because Flask does not automatically load `.env` files, add this line near the top of `app.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

The supplied `app.py` is intentionally ready for this addition.

### 5. Run

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Security

Never upload your real API key to GitHub. Keep it in `.env`; `.gitignore` excludes it from the repository.

## CodeAlpha Requirements Covered

The project provides:
1. A user interface for entering text.
2. Source and target language selection.
3. API-based translation.
4. Clear translated output.
5. An additional copy feature.

## Internship Submission

Repository name should follow the CodeAlpha format:

```text
CodeAlpha_LanguageTranslationTool
```

Before submission, test the project, push the source code to GitHub, record a short project demonstration, and submit the repository/video through the internship submission form.
