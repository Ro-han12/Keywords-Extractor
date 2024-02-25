import streamlit as st
from PIL import Image
import pytesseract
import io
from pdf_extract import extract_text_from_pdf
from Utils.helper import allowed_file, save_uploaded_file
import yake
import os

# Configure YAKE keyword extractor
kw_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=20)

def main():
    st.title("PDF and Text Analysis")
    
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file:
        file_type = st.radio("Select File Type", ["PDF", "Image"])

        if st.button("Submit"):
            try:
                file_contents = uploaded_file.read()

                # Initialize extracted_text with an empty string
                extracted_text = ""

                if file_type == 'Image':
                    # Preprocess the image before OCR
                    preprocessed_image = preprocess_image(file_contents)

                    # Perform OCR using Pytesseract
                    extracted_text = pytesseract.image_to_string(preprocessed_image)
                elif file_type == 'PDF':
                    # Save the uploaded PDF file temporarily
                    pdf_path = "temp.pdf"
                    with open(pdf_path, "wb") as f:
                        f.write(file_contents)

                    # Extract text from the PDF
                    extracted_text = extract_text_from_pdf(pdf_path)

                    # Remove the temporary PDF file
                    os.remove(pdf_path)

                # Extract keywords using YAKE
                keywords = kw_extractor.extract_keywords(extracted_text)
                extracted_keywords = [keyword[0] for keyword in keywords]

                st.subheader("Extracted Text:")
                st.write(extracted_text)

                st.subheader("Extracted Keywords:")
                if extracted_keywords:
                    for keyword in extracted_keywords:
                        st.write(keyword)
                else:
                    st.write("No keywords extracted.")
            except Exception as e:
                st.error(f"Error: {e}")

def preprocess_image(image_data):
    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_data))

    # Additional preprocessing steps (if needed)
    # For example, resizing, grayscale conversion, denoising, etc.
    
    # Return the preprocessed image data
    return image

if __name__ == "__main__":
    main()
