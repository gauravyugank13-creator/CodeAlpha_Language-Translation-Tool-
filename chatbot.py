"""
FAQ CHATBOT WITH NLP
To run this locally:
  streamlit run chatbot.py

Make sure you've installed dependencies:
  pip install -r requirements.txt
"""

import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import random

# Download NLTK data on first run
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Load intents
with open('intents.json', 'r') as f:
    intents_data = json.load(f)

# Setup
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
CONFIDENCE_THRESHOLD = 0.25


def preprocess_text(text):
    """Tokenize, remove stopwords, and lemmatize"""
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens 
              if word.isalnum() and word not in stop_words]
    return ' '.join(tokens)


def build_vectorizer_and_data():
    """Build TF-IDF vectorizer from patterns"""
    patterns = []
    intent_tags = []
    
    for intent in intents_data['intents']:
        for pattern in intent['patterns']:
            patterns.append(preprocess_text(pattern))
            intent_tags.append(intent['tag'])
    
    vectorizer = TfidfVectorizer()
    vectorizer.fit(patterns)
    
    return vectorizer, patterns, intent_tags


def find_intent(user_input, vectorizer, patterns, intent_tags):
    """Find matching intent using cosine similarity"""
    processed_input = preprocess_text(user_input)
    input_vector = vectorizer.transform([processed_input])
    patterns_vectors = vectorizer.transform(patterns)
    
    similarities = cosine_similarity(input_vector, patterns_vectors)[0]
    best_match_idx = similarities.argmax()
    best_score = similarities[best_match_idx]
    
    if best_score >= CONFIDENCE_THRESHOLD:
        return intent_tags[best_match_idx], best_score
    else:
        return None, best_score


def get_response(intent_tag):
    """Get random response for matched intent"""
    for intent in intents_data['intents']:
        if intent['tag'] == intent_tag:
            return random.choice(intent['responses'])
    return "I'm sorry, I don't understand. Could you rephrase that?"


# Build vectorizer once
vectorizer, patterns, intent_tags = build_vectorizer_and_data()

# Streamlit UI
st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 FAQ Chatbot")

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# User input
user_input = st.chat_input("Ask me something...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.write(user_input)
    
    # Find intent and generate response
    intent_tag, confidence = find_intent(user_input, vectorizer, patterns, intent_tags)
    
    if intent_tag:
        response = get_response(intent_tag)
    else:
        response = "I'm sorry, I don't understand. Could you rephrase that?"
    
    # Add bot response to history
    st.session_state.messages.append({'role': 'assistant', 'content': response})
    with st.chat_message('assistant'):
        st.write(response)


# =====================================================
# QUICK TEST (Run with: python -m chatbot)
# =====================================================
if __name__ == "__main__":
    print("\n=== Chatbot NLP Test ===")
    
    test_questions = [
        "hello",
        "what time do you open",
        "where is your office",
        "how can i contact you",
        "bye",
    ]
    
    print("\nTesting intent matching:")
    for question in test_questions:
        intent, score = find_intent(question, vectorizer, patterns, intent_tags)
        response = get_response(intent) if intent else "I don't understand"
        print(f"Q: {question}")
        print(f"   Intent: {intent} (confidence: {score:.2f})")
        print(f"   Response: {response}\n")
    
    print("Note: To see the full Streamlit UI, run: streamlit run chatbot.py")
