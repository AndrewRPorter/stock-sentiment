from flask import (Blueprint, Response, current_app, redirect, render_template,
                   request, session)

from ..database import DBInterface
from ..forms import SentimentForm
from ..sentiment import classify

main_bp = Blueprint("main", __name__, url_prefix="/")


@main_bp.route("/", methods=["GET", "POST"])
def index() -> Response:
    user = None
    form = SentimentForm()

    if "id" in request.cookies:
        user = DBInterface.get_user(request.cookies.get("id"))

    if form.validate_on_submit():
        text = form.text.data

        if text == "":
            return render_template("index.html")
        else:
            sentiment, confidence = classify.get_sentiment_info(text)

            return render_template(
                "index.html",
                form=form,
                sentiment=sentiment,
                confidence=confidence,
                user=user,
            )
    elif request.method == "POST":
        # TODO log form errors here? if form.errors ...
        if "csrf_token" not in session:
            session["csrf_token"] = form.csrf_token.data

        return render_template("index.html", form=form, user=user)

    return render_template("index.html", form=form, user=user)


@main_bp.route("/about", methods=["GET"])
def about() -> Response:
    user = None

    if "id" in request.cookies:
        user = DBInterface.get_user(request.cookies.get("id"))

    return render_template("about.html", user=user)


@main_bp.route("/api", methods=["GET"])
def api() -> Response:
    user = None

    if "id" in request.cookies:
        user = DBInterface.get_user(request.cookies.get("id"))

    return render_template("api.html", user=user)


@main_bp.route("/profile", methods=["GET"])
def profile() -> Response:
    user = None

    if "id" in request.cookies:
        user = DBInterface.get_user(request.cookies.get("id"))
        return render_template("profile.html", user=user)

    return redirect("/")


@main_bp.route("/logout", methods=["GET"])
def logout() -> Response:
    """Reset cookies on logout"""
    response = current_app.make_response(redirect("/"))
    response.delete_cookie("first_name")
    response.delete_cookie("id")
    return response
