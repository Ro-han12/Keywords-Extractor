import spacy
import re 
nlp=spacy.load("en_core_web_sm")
def extract_keywords(text):
    doc=nlp(text)
    keywords=[chunk.text for chunk in doc.noun_chunks]
    #extracting keywords with criteria
    return keywords