from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    BooleanField,
    SubmitField,
    TextAreaField,
    FieldList,
    FormField,
)
from wtforms.validators import DataRequired, ValidationError
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import Recipe, Ingredient, Step


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
