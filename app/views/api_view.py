import time

from flask import Blueprint, Response, jsonify, request

from ..database import DBInterface
from ..sentiment import classify
from ..tools import fetcher

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/1.0/<string:ticker>", methods=["GET"])
def get_sentiment(ticker: str) -> Response:
    timestamp = time.time()
    key = request.args.get("key", None)

    if not key:
        return jsonify({"error": "No API key provided", "timestamp": timestamp})
    elif not DBInterface.valid_key(key):
        return jsonify({"error": "Invalid API key provided", "timestamp": timestamp})

    # check to see if the input ticker is valid or not
    if not fetcher.invalid(ticker):
        payload = fetcher.get_all_news(ticker)
        articles = payload["articles"]

        data = []
        number_neutral = 0
        number_positive = 0
        number_negative = 0
        avg_sent = "neutral"
        total_conf = 0.0  # total confidence count

        for article in articles:
            if all(key in article for key in ("title", "description", "url")):

                if not (
                    article["description"]
                ):  # temporary workaround for articles with no description
                    continue

                sentiment, confidence = classify.get_sentiment_info(
                    article["description"]
                )

                new_sentiment = {
                    "article": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "sentiment": sentiment,
                    "confidence": confidence,
                }

                total_conf += float(confidence)  # implicit conversion

                if sentiment == "positive":
                    number_positive += 1
                elif sentiment == "negative":
                    number_negative += 1
                else:
                    number_neutral += 1

                data.append(new_sentiment)

        if len(data) == 0:
            return jsonify(
                {
                    "totalResults": len(data),
                    "results": data,
                    "ticker": ticker,
                    "timestamp": timestamp,
                }
            )

        # determine average sentiment
        if (number_positive - number_negative) > number_neutral:
            avg_sent = "positive"
        elif (number_negative - number_positive) > number_neutral:
            avg_sent = "negative"

        return jsonify(
            {
                "totalResults": len(data),
                "results": data,
                "ticker": ticker.upper(),
                "averageSentiment": avg_sent,
                "averageConfidence": total_conf / len(data),
                "timestamp": timestamp,
            }
        )

    return jsonify(
        {
            "error": f"'{ticker}' is not recognized",
            "ticker": ticker,
            "timestamp": timestamp,
        }
    )
