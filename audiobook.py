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

# Function to convert text to speech using edge_tts
async def text_to_speech(text, output_file):
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural", verify=False)
    await communicate.save(output_file)

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
        st.write(text)  # Display extracted text
        
        output_file = "output.mp3"
        asyncio.run(text_to_speech(text, output_file))
        
        st.audio(output_file, format='audio/mp3')
