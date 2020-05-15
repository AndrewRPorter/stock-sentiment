from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     TextAreaField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class CSRFForm(FlaskForm):
    class Meta:
        csrf = True


class SentimentForm(CSRFForm):
    """Main index page form implementation with csrf protection"""

    text = TextAreaField(description="", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(CSRFForm):
    """Log in form implementation with CSRF protection"""

    email = EmailField("Email Address", validators=[DataRequired()])
    password = PasswordField("Password", description="", validators=[DataRequired()])
    remember_me = BooleanField("Remember me", default="checked")
    submit = SubmitField("Log in")


class SignupForm(CSRFForm):
    """Sign up form implementation with CSRF protection"""

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired()])
    password = PasswordField("Password", description="", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Re-type Password", description="", validators=[DataRequired()]
    )
    submit = SubmitField("Sign up")


class ResetForm(CSRFForm):
    """Reset form implementation with CSRF protection"""

    email = EmailField("Email Address", validators=[DataRequired()])
    submit = SubmitField("Reset")
