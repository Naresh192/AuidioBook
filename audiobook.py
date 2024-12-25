import streamlit as st
import fitz  # PyMuPDF
import re
from gtts import gTTS
import streamlit.components.v1 as components
import pyttsx3
import tempfile
import os
from pydub import AudioSegment




from concurrent.futures import ThreadPoolExecutor
audio_objects=[]
import time
import io
import base64
import wave
import io
from pydub import AudioSegment
import io

st.markdown("""
    <style>
    audio {
  display: none;
}
    </style>
""", unsafe_allow_html=True)


from mutagen.mp3 import MP3
import io

def get_audio_length(mp3_bytes):
    audio = MP3(io.BytesIO(mp3_bytes))
    return audio.info.length

# Function to convert a sentence to audio
def text_to_audio(sentence, index):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"Voice: {voice.name}, ID: {voice.id}")
    engine.setProperty('rate', 150)    # Speed of speech

    engine.setProperty('voice', voices[1].id)

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False,suffix='.wav')
    temp_file_name = temp_file.name
    engine.save_to_file(sentence, temp_file_name)
    temp_file.close()
    engine.runAndWait()
    # Load the WAV file
    audio = AudioSegment.from_wav(temp_file_name)
    # Calculate the duration in seconds
    duration = len(audio) / 1000.0
    engine.runAndWait()
    f=open(temp_file_name,'rb')
    data=f.read()
    f.close()
    st.write(len(data))
    os.remove(temp_file_name)

    #tts = gTTS(text=sentence, lang='en')
    audio_objects.append((sentence, data,duration))

def split_paragraph_into_sentences(paragraph):
    # Regular expression to match sentence-ending punctuation
    sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
    sentences = sentence_endings.split(paragraph)
    return sentences

# Function to extract text from a PDF page
def extract_text_from_page(pdf_path, page_number):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)  # Page numbers start from 0
    text = page.get_text()
    return text


# Streamlit app
st.title("PDF to Audiobook Converter")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    pdf_path = uploaded_file.name
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    num_pages = len(fitz.open(pdf_path))
    page_number = st.number_input("Select Page Number", min_value=1, max_value=num_pages, step=1)

    if st.button("Convert to Audio"):
        text = extract_text_from_page(pdf_path, page_number)
        # Example usage
        sentences = split_paragraph_into_sentences(text)

        # Use ThreadPoolExecutor to convert sentences in parallel
        for index, sentence in enumerate(sentences):
                text_to_audio(sentence, index)
        st.write(text)  # Display extracted text
        # Streamlit app to display sentences and play audio
        st.write("Hello")
        st.write(audio_objects)
        for index, (sentence, tts,dur) in enumerate(audio_objects):
            #audio_fp = io.BytesIO()
            #tts.write_to_fp(audio_fp)
            #audio_fp.seek(0)
            # Simulate loading your audio file (replace this with your actual audio data)
            audio_bytes = tts  # Your audio data in bytes
            st.write("Hello")
            # Encode the audio data to base64
            audio_base64 = base64.b64encode(audio_bytes).decode()

            # Send the base64 string to the frontend
            st.markdown(f"""
                <audio id="audio{index}" autoplay>
                    <source src="data:audio/wav;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)
            time.sleep(dur)





