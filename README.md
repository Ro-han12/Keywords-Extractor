## PDF and Text Analysis App

This is a Streamlit web application for analyzing text and PDF files. The application allows users to perform text analysis with or without a Language Model (LLM).

### Features

- **Text Analysis without LLM**: Upload text or image files (PDF, PNG, JPG, JPEG) and analyze the content. Text extraction from PDFs and OCR (Optical Character Recognition) for images are supported. Extracted text is displayed along with keywords extracted using the YAKE keyword extractor.
  
- **Text Analysis with LLM**: Utilizes a Language Model (LLM) to perform advanced text analysis. Users can upload PDF files and specify prompts for analyzing the content. The application provides options to summarize the PDF content and extract important points and keywords.

### How to Use

1. **Choose Analysis Option**: Select one of the available options: "Text Analysis without LLM" or "Text Analysis with LLM".

2. **Upload File**: Upload the file you want to analyze. Supported file types include PDF, PNG, JPG, and JPEG.

3. **Text Analysis**:
    - Without LLM: If selected, the application extracts text from the uploaded file and displays it. Keywords are extracted using the YAKE keyword extractor.
    - With LLM: If selected, users can input prompts for summarizing the PDF content or extracting important points and keywords.

4. **View Results**: The extracted text and keywords are displayed for analysis.

### Libraries Used

- Streamlit: For building the web application interface.
- PIL (Python Imaging Library): For image processing tasks.
- Pytesseract: For OCR (Optical Character Recognition) on images.
- pdf_extract: For extracting text from PDF files.
- yake: For keyword extraction.
- pdf2image: For converting PDF pages to images.
- google.generativeai: For utilizing Language Models (LLM) for text analysis.

### How to Run

To run the application, ensure you have all the required libraries installed. Then, execute the script using the following command:

```bash
streamlit run final.py
```
