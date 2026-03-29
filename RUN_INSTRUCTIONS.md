# Michigan Legal Navigator — Setup & Run Instructions

This is a Flask web application that provides legal assistance for Michigan residents. The chat feature is backed by a RAG pipeline over the full Michigan Compiled Laws (MCL) corpus, stored as a ChromaDB vector database.

---

## Prerequisites

- Python 3.8 or higher
- An API key for at least one supported LLM provider (OpenAI, Google Gemini, or Anthropic Claude)
- An OpenAI API key with access to the Embeddings API (used for query embedding via text-embedding-3-small)
- The pre-built ChromaDB MCL collection (not included in the repository — see note below)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/lcottone-oss/GrizzHacks8.git
cd GrizzHacks8
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the project root. Add keys for whichever provider(s) you plan to use:

```
OPENAI_API_KEY=your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
```

You don't need all three LLM keys — only the one you intend to use. However, an OpenAI API key is always required regardless of your LLM choice, as it is used for embeddings.

**Never commit `.env` to Git.** It is already listed in `.gitignore`.

### 4. Obtain or Build the ChromaDB Collection

The chat feature requires a local ChromaDB persistent collection containing pre-embedded chunks of the full MCL. This collection is not included in the repository because it exceeds 800 MB.

To build it yourself:

1. Scrape the full MCL text from [legislature.mi.gov/documents/mcl/](https://legislature.mi.gov/documents/mcl/)
2. Convert the `.xml` files into `.jsonl` format — each line of the `.jsonl` file corresponds to a single MCL section
3. Chunk the text into segments — each MCL section can generally be used as a single chunk, but some sections are too large for a single API call and need to be broken into smaller segments
4. Embed each chunk using OpenAI's `text-embedding-3-small`
5. Store the embeddings in a ChromaDB persistent collection

---

## Running the App

```bash
python MainPage.py
```

Then open `http://localhost:5000` in your browser.

You should see output like:

```
WARNING: This is a development server. Do not use it in production deployments.
Running on http://127.0.0.1:5000
```

---

## Switching LLM Providers

The chat backend supports OpenAI, Google Gemini, and Anthropic Claude. To switch providers, open `MainPage.py` and go to lines 42–44 — comment in the line for the provider you want and comment out the others. It is a one-line change.

Make sure the corresponding API key is present in your `.env` file.

---

## Project Structure

```
GrizzHacks8/
├── MainPage.py              # Flask app — routes and chat handler
├── laws.json                # Small set of hard-coded MCL facts (fees, deadlines, form URLs)
├── requirements.txt         # Python dependencies
├── .env                     # API keys — not committed
├── RUN_INSTRUCTIONS.md      # This file
├── Templates/
│   ├── base.html
│   ├── index.html           # Main page with chat UI
│   ├── RentersRights.html
│   ├── small_businesses.html
│   ├── p_injury.html
│   └── s_claims.html
└── mcl_chroma_db/              # RAG pipeline over full MCL corpus
                             # ChromaDB collection not committed (>800 MB)
```

**Note on `laws.json`:** This file contains a small number of authoritative figures — filing fees, deposit limits, deadlines, and official SCAO form URLs — injected into the system prompt to prevent the LLM from hallucinating those specifics. It is not the knowledge source for the chat. The ChromaDB collection is.

---

## Troubleshooting

### API key not found

- Confirm `.env` exists in the project root (not in a subdirectory)
- Key names are case-sensitive: `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`
- Restart the Flask server after editing `.env`

### ChromaDB collection not found

- The collection must be built locally before the chat feature will work — it is not in the repository
- Check that the collection path in `MainPage.py` matches where you placed the built database — the expected path is `mcl_chroma_db`

### Port already in use

Modify the last line of `MainPage.py`:

```python
app.run(debug=True, port=5001)
```

### Import errors

```bash
pip install -r requirements.txt
```

---

## Production Deployment

The Flask development server is not suitable for production. For a production setup:

1. Use a WSGI server such as Gunicorn: `gunicorn -w 4 MainPage:app`
2. Set `debug=False` in `MainPage.py`
3. Put a reverse proxy (e.g. Nginx) in front of Gunicorn
4. Manage secrets with a proper secrets manager rather than a `.env` file

---

## Support

Open a GitHub issue at [github.com/lcottone-oss/GrizzHacks8](https://github.com/lcottone-oss/GrizzHacks8/issues).
