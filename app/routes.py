from flask import render_template, request, redirect
from app import app
from app.forms import ContactForm
import csv


@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")


@app.route("/contact_me.html", methods=["GET", "POST"])
def contact_me():
    form = ContactForm()
    if form.validate_on_submit():
        return redirect("form_submitted.html")
    return render_template("contact_me.html", title="Sign In", form=form)


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)
