from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired()], render_kw={"placeholder": "Name"}
    )
    email = EmailField(
        "Email", validators=[DataRequired()], render_kw={"placeholder": "Email"}
    )
    subject = StringField(
        "Subject", validators=[DataRequired()], render_kw={"placeholder": "Subject"}
    )
    copy = BooleanField("Email me a copy")
    message = TextAreaField(
        "Message", validators=[DataRequired()], render_kw={"placeholder": "Message"}
    )
    submit = SubmitField("Send message")
