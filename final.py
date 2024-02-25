import streamlit as st
from PIL import Image
import pytesseract
import io
from experiments.pdf_extract import extract_text_from_pdf
from Utils.helper import allowed_file, save_uploaded_file
import yake
import os

# Configure YAKE keyword extractor
kw_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=20)

def preprocess_image(image_data):
    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_data))

    # Additional preprocessing steps (if needed)
    # For example, resizing, grayscale conversion, denoising, etc.
    
    # Return the preprocessed image data
    return image

# Function for text analysis without LLM
def text_analysis_without_llm():
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

# Function for text analysis with LLM
def text_analysis_with_llm():
    from dotenv import load_dotenv
    load_dotenv()

    import streamlit as st 
    import os 
    import io
    import base64
    from PIL import Image 
    import pdf2image
    import google.generativeai as genai 

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model=genai.GenerativeModel("gemini-pro-vision")
    def get_gemini_response(input,pdf_content,prompt):
        model=genai.GenerativeModel('gemini-pro-vision')
        response=model.generate_content([input,pdf_content[0],prompt])
        return response.text 

    def input_pdf_setup(uploaded_file):
        if uploaded_file is not None:
            images=pdf2image.convert_from_bytes(uploaded_file.read())
            
            first_page=images[0]
            
            
            #convert to bytes
            img_byte_arr=io.BytesIO()
            first_page.save(img_byte_arr,format='JPEG')
            img_byte_arr=img_byte_arr.getvalue()

            pdf_parts=[
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()
                }
            ]
            return pdf_parts
        else:
            raise FileNotFoundError("no file uploaded")
        
    st.header("PDF Q&A")
    input_text=st.text_area("Analyse Pdf",key="input")
    uploaded_file=st.file_uploader("Upload your pdf file",type=['pdf'])

    if uploaded_file is not None:
        st.write("pdf uploaded successfully")
        
    submit1= st.button("Summarize the pdf")
    submit2=st.button("Important text & keywords")

    input_prompt = """
    As an expert pdf text analyser, 
    your task is to analyze text contents in the pdf  and provide the following information in the specified format:
    1. Summarize the whole pdf content in short.
    2. Also highlight  important points and keywords from the pdf. 
    """
    if submit1:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt,pdf_content,input_text)
            st.subheader("the response is ")
            st.write(response)
        else:
            st.write("please uplpad a pdf ")
    elif submit2:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt,pdf_content,input_text)
            st.subheader("the response is ")
            st.write(response)
        else:
            st.write("please uplpad a pdf ")

def main():
    option = st.radio("Choose option:", ["1. Text Analysis without LLM", "2. Text Analysis with LLM"])

    if option == "1. Text Analysis without LLM":
        text_analysis_without_llm()
    elif option == "2. Text Analysis with LLM":
        text_analysis_with_llm()

if __name__ == "__main__":
    main()
