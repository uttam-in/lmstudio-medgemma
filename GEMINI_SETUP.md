# Gemini 2.5 Setup Guide

## Quick Setup

The system has been updated to use Google's Gemini 2.5 API instead of LM Studio.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install the new `langchain-google-genai` package.

### 2. Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 3. Configure API Key

Edit the `.env` file and replace `your_gemini_api_key_here` with your actual API key:

```
GEMINI_API_KEY=AIzaSy...your_actual_key_here
```

### 4. Run the System

```bash
python main.py
```

## Configuration Options

In `config.py`, you can:

- **Switch models**: Change `MODEL_NAME` to use different Gemini models:
  - `gemini-2.0-flash-exp` (default, fast and experimental)
  - `gemini-1.5-pro` (production-ready, more stable)
  - `gemini-1.5-flash` (faster, lower cost)

- **Switch back to LM Studio**: Set `USE_GEMINI = False` to use local LM Studio

## Available Gemini Models

- **gemini-2.0-flash-exp**: Latest experimental model with vision capabilities
- **gemini-1.5-pro**: Production model with excellent multimodal performance
- **gemini-1.5-flash**: Faster, cost-effective option

## Troubleshooting

If you get authentication errors:
1. Verify your API key is correct in `.env`
2. Make sure you have API access enabled in Google AI Studio
3. Check your API quota hasn't been exceeded

If you want to switch back to LM Studio:
1. Set `USE_GEMINI = False` in `config.py`
2. Make sure LM Studio is running on port 1234
