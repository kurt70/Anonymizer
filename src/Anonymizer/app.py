# app.py

from flask import Flask, request, jsonify
from anonymizer import anonymize_text

app = Flask(__name__)

@app.route('/anonymize', methods=['POST'])
def anonymize():
    data = request.get_json()
    text = data.get('text', '')
    anonymized_text = anonymize_text(text)
    return jsonify({'anonymized_text': anonymized_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
