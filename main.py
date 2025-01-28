from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
        return redirect("form_submitted.html")
    else:
        return "Something went wrong."
