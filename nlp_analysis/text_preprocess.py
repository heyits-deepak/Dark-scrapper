import re
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """
    Cleans and tokenizes text for NLP processing.
    """
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    text = ' '.join([token.lemma_ for token in nlp(text) if not token.is_stop])  # Lemmatization & stopword removal
    return text

# Test function
if __name__ == "__main__":
    test_text = "Hacker selling stolen credit card data! Contact now."
    cleaned_text = clean_text(test_text)
    print(f"Cleaned Text: {cleaned_text}")
