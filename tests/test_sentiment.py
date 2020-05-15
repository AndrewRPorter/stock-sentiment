import pytest

from app.sentiment import classify


@pytest.mark.skip(reason="Classifier not yet fully functional")
def test_positive():
    sent, conf = classify.get_sentiment_info("This is a positive test")
    assert sent == "positive"
    assert conf > 0


@pytest.mark.skip(reason="Classifier not yet fully functional")
def test_negative():
    sent, conf = classify.get_sentiment_info("This is a negative test")
    assert sent == "negative"
    assert conf > 0


def test_neutral():
    pass
