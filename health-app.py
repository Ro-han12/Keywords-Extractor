import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def text_analysis_with_llm():
    st.header("PDF Q&A")
    input_text = st.text_area("Analyze PDF", key="input")
    uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf'])

    if uploaded_file:
        st.write("PDF uploaded successfully")
        
    submit1 = st.button("Summarize the PDF")
    submit2 = st.button("Important Text & Keywords")

    input_prompt = """
    As an expert  Health Summary Generator for veterinarians, 
    your task is to analyze text contents in the PDF and Generate a structured health summary report for a veterinary patient. The report should contain separate sections for client information, patient information, clinic information, vaccinations, medical data, medications, laboratory results, and imaging studies. Each section should follow the order and layout provided below, and if any specific detail is unavailable, note 'N/A' for that entry. provide the following information:
    1. Summarize the PDF content in short.
    2. Highlight important points and keywords from the PDF
    """
    if submit1 or submit2:
        if uploaded_file:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt, pdf_content, input_text)
            st.subheader("Response")
            st.write(response)
        else:
            st.write("Please upload a PDF.")

def main():
    text_analysis_with_llm()

if __name__ == "__main__":
    main()
