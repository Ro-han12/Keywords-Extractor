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
    
st.set_page_config(page_title="PDF EXPERT")
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
        st.write("please upload a pdf ")
elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt,pdf_content,input_text)
        st.subheader("the response is ")
        st.write(response)
    else:
        st.write("please upload a pdf ")