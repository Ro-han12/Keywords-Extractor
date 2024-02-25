from keyword_extract import extract_keywords
import re 
import spacy 
nlp=scapy.load('en_core_web_sm')

def extract_entities(text):
    doc=nlp(text)
    entities={
        "name":[],
        "location":[],
        "skills":[],
        "keywords":[]
    }
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            entities['name'].append(ent.text)
        elif ent.label_ == 'GPE':
            entities['location'].append(ent.text)
        elif ent.label_ == 'SKILLS':
            entities['skills'].append(ent.text)
    return  entities 
def extract_phone_numbers(text):
    phone_numbers=re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
    return phone_numbers

def extract_emails(text):
    emails=re.findall(r'\S+@\S+\.\S+', text)
    return emails

def extract_information(text):
    extracted_entities={
        "name":[],
        "location":[],
        "skills":[],
        "keywords":[]
    }
    doc=nlp(text)
    
    skills_list=["Python","Machine Learning","Data Analysis","SQL"]
    for token in doc:
        if token.text in skills_list:
            extracted_entities['skills'].append(token.text)
            
        for ent in doc.ents:
            if ent.label_ == "GPE":
                extracted_entities["location"].append(ent.text)
                
        extracted_entities['keywords']=extract_keywords(text)
        return extracted_entities