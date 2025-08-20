# Streamlit Cloud Deployment Guide

## Prerequisites

1. **GitHub Repository**: Your code must be in a public GitHub repository
2. **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Environment Variables**: Configure your API keys in Streamlit Cloud

## Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Fix deployment dependencies"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Set the main file path to: `app.py`
5. Click "Deploy"

### 3. Configure Environment Variables

In your Streamlit Cloud app settings, add these environment variables:

```
GEMINI_API_KEY=your-actual-gemini-api-key
APP_TITLE=AI Intelligent Prompt Generator
APP_DESCRIPTION=Generate structured prompts for various departments using AI agents
DEFAULT_DEPARTMENT=General
LOG_LEVEL=INFO
```

## Troubleshooting

### Common Issues

1. **Dependency Installation Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check for version conflicts
   - Use compatible versions for Streamlit Cloud

2. **Import Errors**
   - Verify all import paths are correct
   - Check for missing `__init__.py` files
   - Ensure relative imports work in deployment environment

3. **Environment Variable Issues**
   - Double-check API key configuration
   - Verify variable names match code expectations
   - Test locally with `.env` file first

4. **Memory/Resource Issues**
   - Streamlit Cloud has memory limits
   - Optimize large imports or data processing
   - Consider lazy loading for heavy dependencies

### Files Structure for Deployment

```
xerago_ai_assistant/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── agents/
│   ├── __init__.py
│   ├── gemini_agents.py     # Main AI agents
│   └── prompt_agents.py     # CrewAI agents (optional)
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── templates/
│   ├── __init__.py
│   └── prompt_templates.py
├── config.py                # Configuration
└── history/                 # Generated prompts
```

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your-api-key

# Run locally
streamlit run app.py
```

## Performance Optimization

1. **Lazy Loading**: Import heavy modules only when needed
2. **Caching**: Use `@st.cache_data` for expensive operations
3. **Session State**: Minimize session state usage
4. **API Calls**: Implement proper error handling and timeouts

## Security Notes

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use Streamlit Cloud's secure environment variable system
3. **Input Validation**: Validate all user inputs
4. **Rate Limiting**: Implement rate limiting for API calls
