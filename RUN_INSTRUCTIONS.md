# Michigan Legal Navigator - Setup & Run Instructions

This is a Flask web application that provides legal assistance for Michigan residents using the Gemini AI API.

## Prerequisites

- Python 3.8 or higher
- Git (for cloning and version control)
- A Gemini API key (free from Google AI Studio)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/lcottone-oss/GrizzHacks8.git
cd GrizzHacks8
```

### 2. Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### 3. Create a `.env` File

In the project root directory, create a file named `.env` and add:

```
GEMINI_API_KEY=your-api-key-here
```

Replace `your-api-key-here` with the actual API key you obtained in step 2.

**Important:** Never commit the `.env` file to GitHub. It's already in `.gitignore`.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required Python packages:
- Flask (web framework)
- python-dotenv (environment variable management)
- google-generativeai (Gemini API)

## Running the Web App

### Start the Flask Server

```bash
python MainPage.py
```

You should see output like:
```
WARNING: This is a development server. Do not use it in production deployments.
Running on http://127.0.0.1:5000
```

### Access the Application

Open your browser and navigate to:

```
http://localhost:5000
```

### Using the Chatbot

1. Type your legal question in the input field (e.g., "What are renter's rights in Michigan?")
2. Click "Send" or press Enter
3. The AI will respond with an explanation in simple 6th-grade English

## Project Structure

```
GrizzHacks8/
├── MainPage.py              # Flask application & routes
├── laws.json                # Michigan law database
├── .env                      # Environment variables (NOT committed to git)
├── requirements.txt          # Python dependencies
├── RUN_INSTRUCTIONS.md      # This file
├── Templates/
│   ├── base.html            # Base HTML template
│   ├── index.html           # Main chatbot interface
│   ├── RentersRights.html
│   ├── small_businesses.html
│   ├── p_injury.html
│   └── s_claims.html
└── ai-chatbot/              # Imported chatbot module
```

## Key Features

- **Michigan Legal Context**: The chatbot uses `laws.json` as the source of truth for Michigan law
- **Simple Language**: All explanations are in 6th-grade English with legal terms defined
- **Persistent Chat**: Messages are displayed in a scrolling chat window
- **Responsive UI**: Built with Bootstrap for mobile compatibility

## Troubleshooting

### "GEMINI_API_KEY not found" Error

- Check that `.env` file exists in the project root
- Verify the key name is exactly `GEMINI_API_KEY` (case-sensitive)
- The `.env` file should look like: `GEMINI_API_KEY=AIzaSy...`
- Restart the Flask server after adding/modifying `.env`

### Port Already in Use (Error: Address already in use)

If port 5000 is already in use, modify `MainPage.py`:

```python
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Import Errors

Run:
```bash
pip install -r requirements.txt
```

To ensure all dependencies are installed.

## Development

### Adding New Features

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly on `http://localhost:5000`
4. Commit and push your changes
5. Submit a pull request

### Adding New Laws to the Database

Edit `laws.json` and follow this format:

```json
{
  "topic_name": {
    "property_1": "value",
    "property_2": "value",
    "jargon_definition": "Simple explanation of this topic"
  }
}
```

The `get_mi_context()` function in `MainPage.py` automatically formats this data for the AI.

## Deployment

For production deployment, consider:

1. Using a production WSGI server (e.g., Gunicorn)
2. Setting `debug=False` in Flask
3. Using environment-specific configurations
4. Setting up a reverse proxy (e.g., Nginx)
5. Securing the API key with secrets management

## Support

For issues or questions, please open a GitHub issue in the repository.
