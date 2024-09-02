# anonymizer/anonymize.py

import re
import spacy
import os
from transformers import pipeline

# Last inn spaCy-modellen
nlp_spacy = spacy.load("en_core_web_sm")

# Last ned nordisk BERT-modell for NER
nlp_bert = pipeline("ner", model="NordicBERT", tokenizer="NordicBERT")

def anonymize_text(text):
    anonymized_text = text

    # Anonymisering med spaCy-modellen
    doc_spacy = nlp_spacy(text)
    for ent in doc_spacy.ents:
        if ent.label_ == "PERSON":
            anonymized_text = anonymized_text.replace(ent.text, "[ANONYMIZED_PERSON]")
        elif ent.label_ in ["GPE", "LOC"]:
            anonymized_text = anonymized_text.replace(ent.text, "[ANONYMIZED_LOCATION]")
    
    # Anonymisering med BERT-modellen
    entities_bert = nlp_bert(text)
    for entity in entities_bert:
        if entity['entity'] in ['B-PER', 'I-PER']:
            anonymized_text = anonymized_text.replace(entity['word'], "[ANONYMIZED_PERSON]")
        elif entity['entity'] in ['B-LOC', 'I-LOC']:
            anonymized_text = anonymized_text.replace(entity['word'], "[ANONYMIZED_LOCATION]")
    
    # Masker fødselsnummer med regex
    anonymized_text = re.sub(r'\b\d{6} \d{5}\b', '[ANONYMIZED_FNR]', anonymized_text)
    
    # Masker adresser med forbedrede regex-mønstre
    anonymized_text = re.sub(
        r'\b\d{1,5}\s[A-Za-zæøåÆØÅ\s]+(?:\s\d+)?(?:[A-Z]?)\s*,?\s*\d{4}\s[A-Za-zæøåÆØÅ\s]+\b', 
        '[ANONYMIZED_ADDRESS]', 
        anonymized_text
    )
    
    # Masker telefonnummer med regex
    anonymized_text = re.sub(r'\b\d{8,12}\b', '[ANONYMIZED_PHONE]', anonymized_text)
    
    # Masker fødselsdato med regex (fullformat)
    anonymized_text = re.sub(r'\bfødt\s\d{1,2}\.\s[A-Za-zæøåÆØÅ]+\s\d{4}\b', '[ANONYMIZED_BIRTHDATE]', anonymized_text)
    
    # Masker e-poster med regex
    anonymized_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[ANONYMIZED_EMAIL]', anonymized_text)
    
    return anonymized_text

def process_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(input_dir, filename), 'r') as file:
                text = file.read()
            
            anonymized_text = anonymize_text(text)
            
            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, 'w') as file:
                file.write(anonymized_text)
    
    print(f"Anonymisering fullført. Anonymiserte filer lagret i {output_dir}")

if __name__ == '__main__':
    input_dir = '/app/applications'
    output_dir = '/app/anonymized'
    process_files(input_dir, output_dir)
