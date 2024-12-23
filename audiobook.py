import streamlit as st
import fitz  # PyMuPDF
import edge_tts
import asyncio


# Function to extract text from a PDF page
def extract_text_from_page(pdf_path, page_number):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)  # Page numbers start from 0
    text = page.get_text()
    return text

from gtts import gTTS
from pydub import AudioSegment

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save('output.mp3')

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
        # Split the text into smaller chunks
        chunks = text.split('. ')  # Splitting by sentences
        audio_segments = []
        for chunk in chunks:
            tts = gTTS(text=chunk, lang='en')
            audio_io = BytesIO()
            tts.write_to_fp(audio_io)
            audio_io.seek(0)
            audio_segment = AudioSegment.from_file(audio_io, format="mp3")
            audio_segments.append(audio_segment)
        
        # Combine the audio segments
        combined = AudioSegment.empty()
        for segment in audio_segments:
            combined += segment
        st.write(text)  # Display extracted text
        
        output_file = "output.mp3"
        # Export the combined audio file
        combined.export("output.mp3", format="mp3")
        
        # Delete the chunk files
        for file in audio_files:
            os.remove(file)
        
        st.audio(output_file, format='audio/mp3')
