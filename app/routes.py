from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.forms import ContactForm, AddRecipe
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import Recipe, Ingredient, Step
from flask_wtf.csrf import generate_csrf


@app.route("/")
@app.route("/index/")
def index():
    return render_template("index.html")


@app.route("/contact_me", methods=["GET", "POST"])
def contact_me():
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("html_page", page_name="form_submitted"))
    return render_template("contact_me.html", form=form)


@app.route("/list_recipes")
def list_recipes():
    query = sa.select(Recipe).order_by(Recipe.name.asc())
    recipes = db.session.scalars(query).all()
    return render_template(
        "list_recipes.html",
        recipes=recipes,
    )


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    form = AddRecipe()
    form.set_current_recipe(None)

    if form.validate_on_submit():
        recipe = Recipe(name=form.title.data.strip())
        db.session.add(recipe)
        db.session.commit()

        for item in form.ingredients.data:
            ingredient = Ingredient(
                name=item["ingredient"].strip(),
                quantity=item["quantity"].strip(),
                recipe_id=recipe.id,
            )
            db.session.add(ingredient)
            db.session.commit()

        for index, step_body in enumerate(form.steps.data):
            step = Step(number=index, body=step_body["body"], recipe_id=recipe.id)
            db.session.add(step)
            db.session.commit()

        flash("Recipe successfully added!")

        return redirect(url_for("list_recipes"))

    return render_template("add_recipe.html", form=form)


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)  # Get recipe or return 404

    # Pre-fill form with existing recipe data
    form = AddRecipe()
    form.set_current_recipe(recipe)

    if request.method == "GET":

        form.title.data = recipe.name

        # Pre-fill ingredients
        form.ingredients.entries = []
        for ingredient in recipe.list_ingredients():
            form.ingredients.append_entry(
                {
                    "ingredient": ingredient.name,
                    "quantity": ingredient.quantity,
                }
            )

        # Pre-fill steps
        form.steps.entries = []
        for step in recipe.list_steps():
            form.steps.append_entry({"body": step.body})

    else:
        if form.validate_on_submit():

            recipe.name = form.title.data

            Ingredient.query.filter_by(recipe_id=recipe.id).delete()
            Step.query.filter_by(recipe_id=recipe.id).delete()
            db.session.commit()

            for item in form.ingredients.data:
                ingredient = Ingredient(
                    name=item["ingredient"].strip(),
                    quantity=item["quantity"].strip(),
                    recipe_id=recipe.id,
                )
                db.session.add(ingredient)
                db.session.commit()

            for index, step_body in enumerate(form.steps.data):
                step = Step(number=index, body=step_body["body"], recipe_id=recipe.id)
                db.session.add(step)
                db.session.commit()

            flash("Recipe updated successfully!")
            return redirect(url_for("list_recipes"))

    return render_template("add_recipe.html", form=form)


@app.route("/delete_recipe/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)  # Get recipe or return 404

    if request.method == "POST":

        Ingredient.query.filter_by(recipe_id=recipe.id).delete()
        Step.query.filter_by(recipe_id=recipe.id).delete()
        Recipe.query.filter_by(id=recipe.id).delete()
        db.session.commit()

        flash("Recipe deleted successfully!")
        return redirect(url_for("list_recipes"))

    return render_template(
        "delete_recipe.html", recipe=recipe, csrf_token=generate_csrf()
    )


@app.route("/<string:page_name>")
def html_page(page_name):
    # print("hello")
    return render_template(page_name + ".html")
