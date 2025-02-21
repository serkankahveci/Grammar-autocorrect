import spacy
import argparse
import logging
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple
from language_tool_python import LanguageTool
from autocorrect import Speller

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@dataclass
class TextProcessor:
    nlp: spacy.language.Language
    grammar_tool: LanguageTool
    speller: Speller

    @classmethod
    def initialize(cls, language: str = 'en-US') -> 'TextProcessor':
        try:
            nlp = spacy.load("en_core_web_sm")
            grammar_tool = LanguageTool(language)
            speller = Speller(lang=language[:2])
            return cls(nlp=nlp, grammar_tool=grammar_tool, speller=speller)
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise RuntimeError(f"Initialization failed: {str(e)}") from e

    def fix_contractions(self, text: str) -> str:
        contractions = {
            "dont": "don't", 
            "doesnt": "doesn't", 
            "isnt": "isn't", 
            "arent": "aren't", 
            "wasnt": "wasn't", 
            "werent": "weren't",
            # Add common verb forms
            "dont like": "doesn't like",  # Third person singular
            "dont have": "doesn't have",
            "dont want": "doesn't want"
        }
        
        # First pass: fix basic contractions
        for wrong, correct in contractions.items():
            text = re.sub(rf'\b{wrong}\b', correct, text, flags=re.IGNORECASE)
        
        # Second pass: handle subject-verb agreement
        doc = self.nlp(text)
        for token in doc:
            if token.text.lower() == "don't" and token.i > 0:
                subject = doc[token.i - 1]
                if subject.text.lower() in ["he", "she", "it"]:
                    text = text.replace("don't", "doesn't")
        
        return text

    def correct_spelling(self, text: str) -> str:
        # Split text into words
        words = text.split()
        corrected_words = []
        
        for word in words:
            # Don't correct proper nouns or contractions
            if "'" in word or (word and word[0].isupper()):
                corrected_words.append(word)
            else:
                corrected_words.append(self.speller(word))
        
        return " ".join(corrected_words)

    def correct_grammar(self, text: str) -> str:
        return self.grammar_tool.correct(text)

    def process_text(self, text: str) -> Tuple[str, dict]:
        changes = {}
        
        # Step 1: Fix contractions first
        processed = self.fix_contractions(text)
        if processed != text:
            changes['contractions'] = {'original': text, 'corrected': processed}

        # Step 2: Correct spelling
        spelled = self.correct_spelling(processed)
        if spelled != processed:
            changes['spelling'] = {'original': processed, 'corrected': spelled}
            processed = spelled

        # Step 3: Apply grammar corrections last
        grammar = self.correct_grammar(processed)
        if grammar != processed:
            changes['grammar'] = {'original': processed, 'corrected': grammar}
            processed = grammar

        return processed, changes

def main():
    processor = TextProcessor.initialize()
    text = input("Enter text to process: ").strip()
    if not text:
        logger.warning("No input text provided.")
        return

    processed_text, changes = processor.process_text(text)
    print("\n=== Processing Results ===")
    print(f"Original text: {text}")
    print(f"Processed text: {processed_text}")
    if changes:
        print("\nChanges made:")
        for correction_type, change in changes.items():
            print(f"\n{correction_type.title()}:")
            print(f"  Before: {change['original']}")
            print(f"  After:  {change['corrected']}")
    else:
        print("\nNo changes were necessary.")

if __name__ == "__main__":
    main()