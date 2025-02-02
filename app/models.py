from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Recipe(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, index=True, unique=True)

    ingredients: so.WriteOnlyMapped["Ingredient"] = so.relationship(
        back_populates="recipe_q"
    )
    steps: so.WriteOnlyMapped["Step"] = so.relationship(back_populates="recipe_s")

    def list_ingredients(self):
        return (
            db.session.query(Ingredient).filter(Ingredient.recipe_id == self.id).all()
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
    quantity: so.Mapped[Optional[str]] = so.mapped_column(sa.String)
    recipe_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Recipe.id, name="fk_ingredient_recipe"), index=True
    )

    recipe_q: so.Mapped[Recipe] = so.relationship(back_populates="ingredients")


class Step(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    number: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    body: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    recipe_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Recipe.id), index=True)

    recipe_s: so.Mapped[Recipe] = so.relationship(back_populates="steps")
