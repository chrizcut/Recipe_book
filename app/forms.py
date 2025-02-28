from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    BooleanField,
    SubmitField,
    TextAreaField,
    FieldList,
    FormField,
    PasswordField,
)
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import Recipe, Ingredient, Step, User


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


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    # email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("Please use a different username.")

    # def validate_email(self, email):
    #     user = db.session.scalar(sa.select(User).where(User.email == email.data))
    #     if user is not None:
    #         raise ValidationError("Please use a different email address.")


class IngredientForm(FlaskForm):
    class Meta:
        csrf = False

    ingredient = StringField("Ingredient", validators=[DataRequired()])
    quantity = StringField("Quantity", validators=[DataRequired()])


class StepForm(FlaskForm):
    class Meta:
        csrf = False

    body = TextAreaField(
        "Description",
        validators=[DataRequired()],
        render_kw={"placeholder": "Step description"},
    )


class AddRecipe(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    steps = FieldList(FormField(StepForm), min_entries=1)
    submit = SubmitField("Submit")

    def validate_title(self, name):
        if self.current_recipe and name.data != self.current_recipe.name:
            recipe = db.session.scalar(
                sa.select(Recipe).where(Recipe.name == name.data)
            )
            if recipe is not None:
                raise ValidationError("You already have a recipe with this name.")

    def set_current_recipe(self, recipe):
        self.current_recipe = recipe
