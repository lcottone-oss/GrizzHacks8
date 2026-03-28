# AI Chatbot with Persistent Memory

An intelligent conversational AI that remembers information across sessions and provides complete conversation management through an interactive menu system.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)

## Features

### 💭 Persistent Memory System
- Automatically extracts and stores relevant user information
- Remembers context across multiple sessions
- Manual memory management (add, view, delete)
- Smart filtering to store only meaningful information

### 💬 Conversation Management
- Save and resume past conversations
- Auto-generated conversation titles
- Delete individual or all conversations
- Smart filtering (only saves substantial conversations)

### 🔍 Web Search Integration
- Access to current information via OpenAI's web search tool
- Real-time data retrieval during conversations

### 🎯 User-Friendly Interface
- Interactive menu system
- Clean command-line navigation
- Easy conversation and memory management

## How It Works

The chatbot uses OpenAI's Responses API with three key intelligent systems:

1. **Automatic Memory Extraction**: After each conversation, the AI analyzes what information is worth remembering about the user for future interactions

2. **Conversation Persistence**: All conversations are stored using Python's pickle serialization, allowing you to resume any previous chat

3. **Smart Conversation Filtering**: The AI evaluates whether a conversation contains substantial content before saving it, preventing clutter from casual greetings

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Setup

1. Clone the repository:
```bash
git clone https://github.com/kMuhtasim/ai-chatbot-with-memory.git
cd ai-chatbot-with-memory
```

2. Install dependencies:
```bash
pip install openai
```

3. Set up your OpenAI API key:

**Option 1: Environment Variable (Recommended)**
```bash
# Linux/Mac
export OPENAI_API_KEY='your-api-key-here'

# Windows
set OPENAI_API_KEY=your-api-key-here
```

**Option 2: Direct in Code**
Edit `chatbot.py` and uncomment line 5:
```python
client = OpenAI(api_key="your-api-key-here")
```

4. Create the files directory:
```bash
mkdir files
```

## Usage

Run the chatbot:
```bash
python chatbot.py
```

### Main Menu Options
```
Main Menu:
1. Start new conversation
2. All Conversations
3. Manage memories
0. Quit
```

### During Conversation

While chatting:
- Type `quit` - End conversation, save memories, and return to main menu
- The chatbot automatically accesses web search when needed
- All conversation context is maintained throughout the session

### Managing Past Conversations

Navigate to "All Conversations" to:
- Resume any previous conversation
- Delete specific conversations
- Delete all conversations at once

### Managing Memories

Navigate to "Manage memories" to:
- View all stored memories
- Manually add new memories
- Delete specific memories
- Clear all memories

## Project Structure
```
ai-chatbot-with-memory/
├── chatbot.py          # Main application
├── files/
│   ├── memories.bin    # Stored user memories (created automatically)
│   └── chats.bin       # Saved conversations (created automatically)
└── README.md
```

## Technical Implementation

### Memory System
- Uses AI-generated prompts to extract relevant user information
- Stores memories in third-person format for better context
- Prevents duplicate storage of already-known information

### Conversation Storage
- Each conversation includes an AI-generated descriptive title
- Full conversation history preserved for context continuity
- Pickle serialization for simple data persistence

### API Integration
- OpenAI Responses API with GPT-4o model
- Web search tool integration for real-time information
- Context management by prepending memories to each request

## What I Learned Building This

- **State Management**: Handling persistent data across multiple sessions
- **AI Prompt Engineering**: Crafting effective prompts for memory extraction, conversation naming, and content filtering
- **User Experience Design**: Building intuitive menu-based navigation systems
- **Error Handling**: Managing file I/O exceptions and edge cases gracefully
- **API Integration**: Working with OpenAI's modern Responses API and tool system
- **Data Persistence**: Using serialization for simple local storage

## Technical Decisions

**Why Pickle?**
- Rapid prototyping and simplicity
- Native Python support without external dependencies
- Note: For production, would use JSON or a database for security and portability

**Why In-Memory Context Injection?**
- Prepending memories to each API request provides full context
- Simple implementation without managing separate context stores
- Works well for moderate-sized memory sets

**Why AI-Generated Metadata?**
- Conversation titles and memory extraction leverage the model's understanding
- Reduces manual user effort
- Creates more natural, descriptive labels

## Limitations & Future Improvements

**Current Limitations:**
- Local storage only (not accessible across devices)
- Pickle format has security considerations
- No conversation search functionality
- Command-line interface only

**Potential Enhancements:**
- Replace pickle with JSON or SQLite for better security and portability
- Add conversation search and filtering
- Implement cloud storage for multi-device access
- Export conversations to PDF or text format
- Build a web-based user interface
- Add conversation tags and categories
- Support for multiple users/profiles

## Requirements
```
openai>=1.0.0
```

## License

MIT License - feel free to use this project for learning or as a foundation for your own applications.

## Acknowledgments

- Built using OpenAI's Responses API
- Inspired by the need for contextual, persistent AI assistants

---

**Note**: This is a learning project demonstrating AI application development, state management, and API integration. For production use, consider security hardening, proper database implementation, and additional error handling.
