import streamlit as st
import fitz  # PyMuPDF
import re
from gtts import gTTS
import streamlit.components.v1 as components

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

def get_audio_length(audio_bytes):
    audio_fp = io.BytesIO(audio_bytes)
    
    audio = AudioSegment.from_file(io.BytesIO(audio_fp), format="mp3")
    duration = len(audio) / 1000.0  # Duration in seconds
    return duration

# Function to convert a sentence to audio
def text_to_audio(sentence, index):
    tts = gTTS(text=sentence, lang='en')
    audio_objects.append((sentence, tts))
    filename = f"sentence_{index}.mp3"
    tts.save(filename)
    print(f"Saved {filename}")

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

        for i, sentence in enumerate(sentences):
            print(f"{sentence}")
        # Use ThreadPoolExecutor to convert sentences in parallel
        with ThreadPoolExecutor() as executor:
            for index, sentence in enumerate(sentences):
                executor.submit(text_to_audio, sentence, index)
        st.write(text)  # Display extracted text
        # Streamlit app to display sentences and play audio
        
        for index, (sentence, tts) in enumerate(audio_objects):
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            # Simulate loading your audio file (replace this with your actual audio data)
            audio_bytes = audio_fp.read()  # Your audio data in bytes
            dur=get_audio_length(audio_bytes)
            # Encode the audio data to base64
            audio_base64 = base64.b64encode(audio_bytes).decode()

            # Send the base64 string to the frontend
            st.markdown(f"""
                <audio id="audio{index}" autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)
            time.sleep(dur)





