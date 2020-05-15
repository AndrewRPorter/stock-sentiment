from flask import (Blueprint, Response, current_app, redirect, render_template,
                   request, session)

from ..database import DBInterface
from ..forms import LoginForm, ResetForm, SignupForm

auth_bp = Blueprint("auth", __name__, url_prefix="/")


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> Response:
    form = LoginForm()

    if "id" in request.cookies:
        user = DBInterface.get_user(request.cookies.get("id"))
        if user is not None:
            return redirect("/")

    if form.validate_on_submit():
        result = DBInterface.authenticate_user(request.form)

        if "error" in result:
            return render_template("login.html", form=form, error=result["error"])

        user = result["user"]

        response = current_app.make_response(redirect("/"))
        response.set_cookie("first_name", user.first_name)
        response.set_cookie("id", user.id)
        return response
    elif request.method == "POST":
        if "csrf_token" not in session:
            session["csrf_token"] = form.csrf_token.data

        return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup() -> Response:
    form = SignupForm()

    if "id" in request.cookies:
        user = DBInterface.get_user(request.cookies.get("id"))
        if user is not None:
            return redirect("/")

    if form.validate_on_submit():
        result = DBInterface.create_user(request.form)

        if "error" in result:
            return render_template("signup.html", form=form, error=result["error"])

        user = result["user"]

        response = current_app.make_response(redirect("/"))
        response.set_cookie("first_name", user.first_name)
        response.set_cookie("id", user.id)
        return response
    elif request.method == "POST":
        if "csrf_token" not in session:
            session["csrf_token"] = form.csrf_token.data

        return render_template("signup.html", form=form)

    return render_template("signup.html", form=form)


@auth_bp.route("/reset", methods=["GET", "POST"])
def reset() -> Response:
    form = ResetForm()

    if "id" in request.cookies:
        user = DBInterface.get_user(request.cookies.get("id"))
        if user is not None:
            return redirect("/")

    if form.validate_on_submit():
        result = DBInterface.reset_user(request.form)

        if "error" in result:
            return render_template("reset.html", form=form, error=result["error"])
    elif request.method == "POST":
        if "csrf_token" not in session:
            session["csrf_token"] = form.csrf_token.data

        return render_template("reset.html", form=form)

    return render_template("reset.html", form=form)
