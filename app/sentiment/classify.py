from textblob import TextBlob

from .train import get_classifier

CLASSIFY_FILE = "classifier.pickle"


def get_sentiment_info(text):
    """Uses pre-trained classifier to perform sentiment analysis on text"""
    text = text.lower()

    cl = get_classifier()
    blob = TextBlob(text, classifier=cl)
    sentiment = blob.sentiment

    polarity = sentiment.polarity
    # subjectivity = sentiment.subjectivity

    prob_dist = cl.prob_classify(text)

    if polarity >= -1.0 and polarity < -0.5:
        probability = prob_dist.prob("negative") * 100
        probability = round(probability, 3)
        return "negative", probability
    elif polarity <= 1.0 and polarity > 0.5:
        probability = prob_dist.prob("positive") * 100
        probability = round(probability, 3)
        return "positive", probability
    elif polarity == 0:  # bad polarity
        probability = (
            max(
                prob_dist.prob("negative"),
                prob_dist.prob("positive"),
                prob_dist.prob("neutral"),
            )
            * 100
        )
        probability = round(probability, 3)
        return prob_dist.max(), probability
    else:
        probability = prob_dist.prob("neutral") * 100
        probability = round(probability, 3)
        return "neutral", probability
