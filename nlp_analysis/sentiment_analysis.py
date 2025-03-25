from textblob import TextBlob

def analyze_sentiment(text):
    """
    Determines the sentiment of a given text.
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity  # Range: -1 (negative) to 1 (positive)
    
    if polarity < -0.2:
        return "High Risk (Negative Sentiment)"
    elif polarity > 0.2:
        return "Low Risk (Positive Sentiment)"
    else:
        return "Moderate Risk (Neutral Sentiment)"

# Test function
if __name__ == "__main__":
    test_text = "Selling zero-day exploits for hacking Windows."
    sentiment = analyze_sentiment(test_text)
    print(f"Sentiment Analysis: {sentiment}")
