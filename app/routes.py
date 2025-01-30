from flask import render_template, request, redirect, url_for
from app import app
from app.forms import ContactForm
import csv


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


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name + ".html")
