# Michigan Legal Navigator

A web application built at **GrizzHacks 8** that helps Michigan residents understand their legal rights in plain English.

Legal information in the US is technically public but practically inaccessible. The Michigan Compiled Laws (MCL) spans thousands of sections written in dense statutory language. This app makes it conversational — a user types a question, and the system retrieves the relevant sections of actual Michigan law and generates a plain-language answer grounded in those sources.

---

## Features

### Informational Pages

Four dedicated pages cover the most common legal situations Michigan residents encounter, with plain-language explanations and direct links to official Michigan State Court Administrative Office (SCAO) forms:

- **Renter's Rights** — security deposit limits, return deadlines, eviction forms
- **Small Claims** — the $7,000 claim ceiling, filing process, e-filing link
- **Personal Injury** — statute of limitations, mini-tort limits, what to document
- **Small Business** — LARA registration, Match on Main grant info ($25k, April 2026 deadline)

### AI Chat Interface

The chat window is backed by a full retrieval-augmented generation (RAG) pipeline over the entire Michigan Compiled Laws corpus.

**How it works:**

1. The user submits a question in natural language.
2. Before retrieval, the full conversation history is sent to an LLM, which synthesizes it into a single self-contained query. **Why not just embed the latest message or the full chat history?**
   > If the user says "I got hit by a car" in one message, then "What should I do?" in the next — embedding only the latest message gives the embedding model almost nothing to work with, and retrieval quality tanks. But embedding the full chat history isn't the answer either — the vector ends up with too much noise, and irrelevant chunks get pulled in. So instead, the full history is sent to an LLM first, which distills it into a single clean query, and that query is what gets embedded. If the user has multiple unrelated issues, the latest one is prioritized in the final query.
3. The rewritten query is embedded using the OpenAI embeddings API (`text-embedding-3-small`).
4. The embedding is used to query a local ChromaDB collection, which stores pre-computed embeddings for every section of the MCL. ChromaDB's built-in approximate nearest neighbor (ANN) algorithm identifies the most semantically relevant chunks.
5. A dynamic number of retrieved chunks are assembled into a context window and sent to the LLM, which generates a final answer constrained to those sources.
6. The response is written at a plain reading level, with legal terms defined inline as they appear.

**The underlying database** is a ChromaDB persistent collection containing pre-embedded chunks of the full MCL. It is not included in this repository — the collection exceeds 800 MB. See setup instructions below.

**Supported LLM providers:** The chat backend supports OpenAI, Google Gemini, and Anthropic Claude. Switching between them requires changing a single commented line in the backend config — no other code changes needed.

---

## Tech Stack

- **Backend:** Python, Flask
- **RAG / Vector Search:** ChromaDB (persistent client, cosine similarity, ANN retrieval)
- **Embeddings:** OpenAI `text-embedding-3-small`
- **LLM (switchable):** OpenAI / Google Gemini / Anthropic Claude
- **Frontend:** HTML, Bootstrap (Jinja2 templates served by Flask)
- **Config:** `python-dotenv`

---

## Project Structure

```
GrizzHacks8/
├── MainPage.py              # Flask app — routes and chat handler
├── laws.json                # Small set of quick-reference MCL facts (fees, deadlines, links)
├── requirements.txt         # Python dependencies
├── .env                     # API keys — not committed
├── RUN_INSTRUCTIONS.md      # Detailed setup reference
├── Templates/
│   ├── base.html
│   ├── index.html           # Main page with chat UI
│   ├── RentersRights.html
│   ├── small_businesses.html
│   ├── p_injury.html
│   └── s_claims.html
└── ai-chatbot/              # RAG pipeline — ChromaDB collection not included (>800 MB)
```

**Note on `laws.json`:** This file contains a small number of hard-coded, authoritative figures (filing fees, deposit limits, grant deadlines, SCAO form URLs) used to anchor the system prompt in specifics that an LLM might otherwise hallucinate. It is not the knowledge source for the chat — the ChromaDB MCL collection is.

---

## Setup

### Prerequisites

- Python 3.8+
- An API key for whichever LLM provider you intend to use (OpenAI, Gemini, or Anthropic)
- The pre-built ChromaDB MCL collection (not included — must be built or obtained separately)

### Install

```bash
git clone https://github.com/lcottone-oss/GrizzHacks8.git
cd GrizzHacks8
pip install -r requirements.txt
```

### Configure

Create a `.env` file in the project root with keys for whichever provider(s) you plan to use:

```
OPENAI_API_KEY=your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
```

To switch LLM providers, comment in the appropriate line in the backend and comment out the others — one line change.

### ChromaDB Collection

The RAG pipeline requires the pre-embedded MCL collection to be present locally. This is not in the repository due to its size (>800 MB). To build it yourself:

1. Obtain the full MCL text corpus
2. Chunk the text into segments
3. Embed each chunk using `text-embedding-3-small`
4. Store the embeddings in a ChromaDB persistent collection

### Run

```bash
python MainPage.py
```

Then open `http://localhost:5000` in your browser.

---

## Limitations

- **Michigan law only.** The system prompt explicitly refuses questions outside the scope of Michigan law.
- **Not legal advice.** This app provides legal information, not legal counsel. It is not a substitute for an attorney in contested or high-stakes situations.
- **ChromaDB not included.** The MCL vector database must be rebuilt or sourced separately before the chat feature is fully functional.
- **Development server only.** Flask's built-in server is not suitable for production. Use Gunicorn behind a reverse proxy and set `debug=False`.

---

## Built At

**GrizzHacks 8** — March 2026  
Contributors: [@kMuhtasim](https://github.com/kMuhtasim), [@lcottone-oss](https://github.com/lcottone-oss), [@pihoo1220-creator](https://github.com/pihoo1220-creator), [@Tamanna-2100](https://github.com/Tamanna-2100)
