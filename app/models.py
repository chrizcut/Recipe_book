from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    # recipe_id: so.Mapped[int] = so.mapped_column(
    #     sa.ForeignKey(Recipe.id, name="fk_ingredient_recipe"), index=True
    # )

    recipes: so.WriteOnlyMapped["Recipe"] = so.relationship(back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Recipe(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer)
    name: so.Mapped[str] = so.mapped_column(sa.String, index=True)
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(User.id, name="fk_recipe_user"), index=True
    )

    __table_args__ = (sa.PrimaryKeyConstraint("user_id", "id", name="pk_recipe"),)

    ingredients: so.WriteOnlyMapped["Ingredient"] = so.relationship(
        back_populates="recipe_q"
    )
    steps: so.WriteOnlyMapped["Step"] = so.relationship(back_populates="recipe_s")

    user: so.Mapped[User] = so.relationship(back_populates="recipes")

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
