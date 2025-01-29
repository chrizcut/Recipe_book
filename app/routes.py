from flask import render_template, request, redirect
from app import app
import csv


@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")


@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    if request.method == "POST":
        data = request.form.to_dict()
        with open("database.csv", "a", newline="") as csvfile:
            fieldnames = ["name", "email", "subject", "copy", "message"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow(
                {
                    "name": data["name"],
                    "email": data["email"],
                    "subject": data["subject"],
                    "copy": data.get("copy", False),
                    "message": data["message"],
                }
            )
        return redirect("form_submitted.html")
    else:
        return "Something went wrong."


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)
