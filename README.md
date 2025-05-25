# TermChat 🤖

A simple and elegant terminal AI chat application that connects to OpenRouter for access to multiple AI models.

## Features

- 🎯 **Multiple AI Models**: Switch between Claude, GPT, Llama, and more
- 🎨 **Beautiful Terminal UI**: Rich formatting with colors and panels
- 💬 **Conversation Memory**: Maintains context throughout your chat session
- ⚡ **Streaming Responses**: See AI responses as they're generated
- 🔧 **Easy Commands**: Simple slash commands for control
- 🚀 **Fast Setup**: Get started in seconds with UV

## Quick Start

### 1. Install Dependencies

Make sure you have [UV](https://docs.astral.sh/uv/) installed, then run:

```bash
uv sync
```

### 2. Set Up Your API Key

1. Get an API key from [OpenRouter](https://openrouter.ai/)
2. Copy the example environment file:
   ```bash
   cp env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

### 3. Run the App

```bash
uv run termchat.py
```

## Usage

### Basic Chat
Just type your message and press Enter to chat with the AI!

### Commands
- `/help` - Show help and available commands
- `/model` - Change the AI model (Claude, GPT, Llama, etc.)
- `/clear` - Clear conversation history
- `/quit` - Exit the application

### Keyboard Shortcuts
- `Ctrl+C` during AI response - Interrupt the current response
- `Ctrl+C` at prompt - Exit the application

## Available Models

The app includes popular models from OpenRouter:

- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Haiku
- **OpenAI**: GPT-4o, GPT-4o Mini, GPT-3.5 Turbo
- **Meta**: Llama 3.1 8B (Free)
- **Microsoft**: WizardLM 2 8x22B
- **Google**: Gemini Pro 1.5
- **Mistral**: Mistral 7B (Free)

## Configuration

You can customize the default model by setting it in your `.env` file:

```
DEFAULT_MODEL=change_default_model_here
```

## Dependencies

- `openai` - For OpenRouter API communication
- `rich` - For beautiful terminal formatting
- `python-dotenv` - For environment variable management

## Tips

- Use `/model` to switch between different AI models for different tasks
- The conversation history is maintained until you use `/clear`
- Free models are available if you want to test without costs
- Responses are streamed in real-time for a better experience

## Troubleshooting

**"OPENROUTER_API_KEY not found"**
- Make sure you've created a `.env` file with your API key

**"Error: ..."**
- Check your internet connection
- Verify your OpenRouter API key is valid
- Some models may have usage limits

## License

MIT License - feel free to modify and use as you like!

---

Enjoy chatting with AI in your terminal! 🚀 