from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Recipe(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, index=True, unique=True)

    quantities_recipe: so.WriteOnlyMapped["Quantity"] = so.relationship(
        back_populates="recipe_q"
    )
    steps: so.WriteOnlyMapped["Step"] = so.relationship(back_populates="recipe_s")

    def list_ingredients(self):
        return (
            db.session.query(Ingredient)
            .join(Quantity, Quantity.ingredient_id == Ingredient.id)
            .filter(Quantity.recipe_id == self.id)
            .all()
        )

    def quantity_ingredient(self, ingredient):
        return (
            db.session.query(Quantity.quantity)
            .filter(
                Quantity.recipe_id == self.id, Quantity.ingredient_id == ingredient.id
            )
            .scalar()
        )

    def list_steps(self):
        return (
            db.session.query(Step)
            .filter(Step.recipe_id == self.id)
            .order_by(Step.number)
            .all()
        )

    def __repr__(self):
        return "Recipe n° " + str(self.id) + ": " + self.name


class Ingredient(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String)

    quantities_ingredients: so.WriteOnlyMapped["Quantity"] = so.relationship(
        back_populates="ingredients_q"
    )


class Quantity(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    quantity: so.Mapped[str] = so.mapped_column(sa.String)
    recipe_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Recipe.id), index=True)
    ingredient_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Ingredient.id), index=True
    )

    recipe_q: so.Mapped[Recipe] = so.relationship(back_populates="quantities_recipe")
    ingredients_q: so.Mapped[Ingredient] = so.relationship(
        back_populates="quantities_ingredients"
    )


class Step(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    number: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    body: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    recipe_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Recipe.id), index=True)

    recipe_s: so.Mapped[Recipe] = so.relationship(back_populates="steps")
