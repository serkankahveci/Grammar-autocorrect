import spacy
from language_tool_python import LanguageTool
from autocorrect import Speller

def initialize_tools():
    """
    Initialize the grammar correction and spelling tools.
    """
    grammar_tool = LanguageTool('en-US')
    speller = Speller(lang='en')
    return grammar_tool, speller

def lemmatize_verbs(text, nlp):
    """
    Lemmatize verbs in the input text using spaCy.
    """
    doc = nlp(text)
    return ' '.join([token.lemma_ if token.pos_ == 'VERB' else token.text for token in doc])

def correct_spelling(text, speller):
    """
    Correct spelling errors in the input text using the Speller tool.
    """
    return speller(text)

def correct_grammar(text, grammar_tool):
    """
    Correct grammatical errors in the input text using LanguageTool.
    """
    return grammar_tool.correct(text)

def process_text(text, nlp, grammar_tool, speller):
    """
    Perform text processing by lemmatizing verbs, correcting spelling,
    and correcting grammar in sequential steps.
    """
    text_with_corrected_tense = lemmatize_verbs(text, nlp)
    text_with_corrected_spelling = correct_spelling(text_with_corrected_tense, speller)
    fully_corrected_text = correct_grammar(text_with_corrected_spelling, grammar_tool)
    return fully_corrected_text

def main():
    """
    Main function to process user input and display the corrected output.
    """
    nlp = spacy.load("en_core_web_sm")
    grammar_tool, speller = initialize_tools()

    user_input = input("Enter a sentence: ")

    corrected_text = process_text(user_input, nlp, grammar_tool, speller)

    if corrected_text.strip() != user_input.strip():
        print("Original:", user_input)
        print("Corrected:", corrected_text)
    else:
        print("No corrections were needed. The input sentence is already correct.")

if __name__ == "__main__":
    main()
