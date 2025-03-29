from transformers import pipeline

# Load AI-powered text classifier
classifier = pipeline("text-classification", model="distilbert-base-uncased")

def classify_text(text):
    """
    Classifies dark web discussions into categories like malware, exploits, or leaks.
    """
    result = classifier(text)
    return result[0]['label']

# Test function
if __name__ == "__main__":
    test_text = "Selling remote access trojans (RATs) for cheap."
    category = classify_text(test_text)
    print(f"Threat Category: {category}")
