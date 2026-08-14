import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure vader_lexicon is downloaded safely
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    try:
        nltk.download('vader_lexicon', quiet=True)
    except Exception:
        pass


def analyze_sentiment_text(text: str) -> str:
    """
    Analyzes input text and returns sentiment classification: positive, neutral, or negative.
    """
    if not text:
        return "neutral"

    try:
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(text)
        compound = scores.get('compound', 0.0)

        if compound >= 0.05:
            return "positive"
        elif compound <= -0.05:
            return "negative"
        else:
            return "neutral"
    except Exception:
        # Simple rule-based fallback if VADER lexicon fails to load
        text_lower = text.lower()
        pos_words = {'good', 'great', 'excellent', 'amazing', 'awesome', 'best', 'love', 'nice', 'perfect', 'happy'}
        neg_words = {'bad', 'terrible', 'worst', 'horrible', 'poor', 'hate', 'awful', 'slow', 'broken', 'disappointed'}

        pos_count = sum(1 for w in pos_words if w in text_lower)
        neg_count = sum(1 for w in neg_words if w in text_lower)

        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        return "neutral"
