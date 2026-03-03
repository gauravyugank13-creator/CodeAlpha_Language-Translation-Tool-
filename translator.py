import streamlit as st
from googletrans import Translator
from gtts import gTTS
import io
import asyncio

# Language codes mapping
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Korean": "ko",
    "Arabic": "ar",
    "Hindi": "hi",
}

def translate_text(text, source_lang, target_lang):
    """Translate text using Google Translate"""
    try:
        translator = Translator()
        # Newer googletrans uses async, but we can use run_sync for compatibility
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(translator.translate(text, src_lang=source_lang, dest=target_lang))
        loop.close()
        # Result is a Translated namedtuple with .text attribute
        return result.text
    except Exception as e:
        return f"Translation error: {str(e)}"

def text_to_speech(text, lang_code):
    """Convert text to speech and return audio bytes"""
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        st.error(f"Audio generation failed: {str(e)}")
        return None

# Page setup
st.set_page_config(page_title="Language Translator", page_icon="globe", layout="centered")
st.title("Language Translator")
st.write("Translate text and listen to it in different languages")

# Input section
col1, col2 = st.columns(2)

with col1:
    source_lang_name = st.selectbox("From:", list(LANGUAGES.keys()), index=0)
    source_lang_code = LANGUAGES[source_lang_name]

with col2:
    target_lang_name = st.selectbox("To:", list(LANGUAGES.keys()), index=1)
    target_lang_code = LANGUAGES[target_lang_name]

# Text input
text_input = st.text_area("Text to translate:", placeholder="Enter text here", height=100)

# Translate button
if st.button("Translate", use_container_width=True):
    if text_input.strip():
        with st.spinner("Translating..."):
            # Get translation
            translated = translate_text(text_input, source_lang_code, target_lang_code)
            st.success("Done!")
            
            # Display result
            st.subheader("Translation:")
            st.code(translated)
            
            # Generate and play audio
            audio = text_to_speech(translated, target_lang_code)
            if audio:
                st.subheader("Listen:")
                st.audio(audio, format="audio/mp3")
    else:
        st.warning("Please enter some text to translate")

st.divider()
st.caption("Powered by Google Translate and gTTS")


# QUICK TEST
if __name__ == "__main__":
    print("\n=== Translator Test ===")
    try:
        test_text = "Hello, how are you?"
        result = translate_text(test_text, "en", "es")
        print(f"EN to ES: {result}")
        
        result = translate_text(test_text, "en", "fr")
        print(f"EN to FR: {result}")
        
        print("Translation working!")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTo run the Streamlit UI, use: streamlit run translator.py")
