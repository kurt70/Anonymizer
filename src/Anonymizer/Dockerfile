# Dockerfile

# Bruk en base image som har Python
FROM python:3.9-slim

# Sett arbeidskatalog
WORKDIR /app

# Kopier kravfiler og installer avhengigheter
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Kopier applikasjonskode og anonymiseringskode
COPY app.py app.py

# Installer spaCy-modellen
RUN python -m spacy download en_core_web_sm

# Installer transformers og modellen
RUN pip install --no-cache-dir transformers
RUN python -c "from transformers import pipeline; pipeline('ner', model='NordicBERT')"

# Sett kommando for å kjøre anonymisering
CMD ["python", "anonymizer/anonymize.py"]
