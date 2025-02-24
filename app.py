from flask import Flask, render_template, request, jsonify
import spacy
from language_tool_python import LanguageTool
from autocorrect import Speller

app = Flask(__name__)

# Initialize text processing tools
nlp = spacy.load("en_core_web_sm")
grammar_tool = LanguageTool("en-US")
speller = Speller(lang='en')

def process_text(text):
    """
    Process input text by correcting grammar and spelling.
    """
    corrected_spelling = speller(text)
    corrected_grammar = grammar_tool.correct(corrected_spelling)
    return corrected_grammar

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    text = request.form.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    corrected_text = process_text(text)
    return jsonify({'corrected_text': corrected_text})

if __name__ == '__main__':
    app.run(debug=True)