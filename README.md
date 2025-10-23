# Task4 for MockPS
Short description

- What it does: Runs a Streamlit web app that accepts user financial questions, uses a Google Generative AI LLM to produce an answer plus extracted key financial terms, displays the chat, and appends a minimal conversation record to `financial_conversations.csv`.

Requirements

- Python 3.10+ (recommended)
- The app uses these Python packages: streamlit, pandas, python-dotenv, pydantic, and a Google generative LLM client (`langchain_google_genai` import in code).
- A Gemini/Google generative API key set in the environment as `GEMINI_API_KEY` or placed into a `.env` file.

Files

- `task.py` — Streamlit app (this file).
- `financial_conversations.csv` — created/updated in the same folder; stores id, timestamp, question, and key_terms.

How to run (Terminal):
1. Provide your API key (one of these options):

- Create a `.env` file in the project root with:

```text
GEMINI_API_KEY=your_api_key_here
```

2. Start the app:

```text
streamlit run task.py
```

5. Open the app in your browser at: http://localhost:8501 (Streamlit's default)

Behavior summary (concise)

- User types a question into the chat box.
- The app sends the question to a structured LLM wrapper expecting a JSON object with fields `answer` and `key_terms`.
- The LLM answer is shown in the chat. Key terms are recorded.
- A one-line record is appended to `financial_conversations.csv` with columns: `id`, `timestamp`, `question`, `key_terms`.

Notes & troubleshooting

- If the LLM client import fails, confirm the package name for the Google generative client and install it.
- If responses return an error message, ensure `GEMINI_API_KEY` is correct and reachable.
- The app does not perform access control or validation on user inputs; treat it as a demo/prototype.

