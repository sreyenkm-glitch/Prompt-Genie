# AI Intelligent Prompt Generator

An intelligent prompt generation system that helps employees create structured, well-defined prompts for various departments using AI agents.

## Features

- **Department-Specific Prompt Generation**: Tailored prompts for different company departments
- **AI Agent-Based Processing**: Uses CrewAI agents for intelligent prompt creation
- **Open Source LLM Integration**: Powered by Ollama and open-source language models
- **User-Friendly Interface**: Clean Streamlit web application
- **Zero Manual Effort**: Fully automated prompt generation process

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, CrewAI, LangChain
- **AI Models**: Ollama (open-source LLMs)
- **Architecture**: Agent-based system

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd xerago_ai_assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Ollama (if not already installed):
   - Visit [Ollama.ai](https://ollama.ai) for installation instructions
   - Pull a model: `ollama pull llama2`

4. Set up environment variables:
```bash
cp env_example.txt .env
# Edit .env with your configuration
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided URL

3. Select your department and provide task details

4. Generate structured prompts with AI assistance

## Project Structure

```
xerago_ai_assistant/
├── app.py                 # Main Streamlit application
├── agents/               # CrewAI agents
├── templates/            # Prompt templates
├── utils/               # Utility functions
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── .env                # Environment variables
```

## Configuration

The application uses environment variables for configuration. See `env_example.txt` for available options.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
