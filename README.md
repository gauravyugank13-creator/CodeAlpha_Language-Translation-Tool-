# CodeAlpha Project

Two simple apps built with Streamlit:

## Task 1: Language Translator (`translator.py`)

Translate text to 12 different languages and listen to pronunciations.

**To run:**
```bash
streamlit run translator.py
```

**Features:**
- Google Translate API (googletrans)
- Text-to-speech with gTTS
- Copy button built into the code block
- Simple dropdown to select languages

**To test the translation logic without UI:**
```bash
python translator.py
```

## Task 2: FAQ Chatbot (`chatbot.py`)

Smart chatbot that understands questions using NLP.

**To run:**
```bash
streamlit run chatbot.py
```

**Features:**
- Loads FAQ patterns from `intents.json`
- Uses NLTK for text processing (tokenize, lemmatize, remove stopwords)
- TF-IDF vectorization + cosine similarity matching
- Confidence threshold to avoid bad matches
- Conversation history with Streamlit chat interface

**To test the NLP logic without UI:**
```bash
python -m chatbot
```

or

```bash
python chatbot.py
```

## Setup

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate it (Windows):
```bash
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run either app:
```bash
streamlit run translator.py
streamlit run chatbot.py
```

## Files

- `requirements.txt` - Python dependencies
- `translator.py` - Language translation app
- `chatbot.py` - FAQ chatbot with NLP
- `intents.json` - FAQ data for the chatbot

That's it! Both scripts have testing sections built in if you need to verify things without the UI.
