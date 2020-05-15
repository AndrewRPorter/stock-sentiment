"""
This file servers both as the application factory and makes the `app`
directory a package
"""
from flask import Flask, g, redirect, render_template

from .sentiment import train
from .views.api_view import api_bp
from .views.auth_view import auth_bp
from .views.main_view import main_bp


def page_not_found(e):
    """Custom error handling"""
    return redirect("/")


def unknown_error(e):
    """Custom error handling"""
    return render_template("error.html"), 500


def create_app(test_config=None, testing=False, debug=False):
    """creates and configures the app"""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("app.config")

    train.setup()  # set up the classifier data if not yet pickled

    app.hash_seed = 8972319

    @app.before_request
    # pylint: disable=W0612
    def before_request():
        """Set global application context information"""
        g.hash_seed = app.hash_seed
        g.app = app

    # register views
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # register error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, unknown_error)

    app.app_context().push()  # this is needed for application global context

    return app


application = create_app()
