from flask import Blueprint, render_template, request, redirect
from ..database import get_db

main = Blueprint("main", __name__)


# HOME
@main.route("/")
def home():
    return redirect("/login")


# QUERY FORM
@main.route("/query", methods=["GET", "POST"])
def query_form():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        query = request.form["query"]

        db = get_db()

        db.execute(
            "INSERT INTO queries (name, email, query, status) VALUES (?, ?, ?, ?)",
            (name, email, query, "Pending")
        )

        db.commit()

        return redirect("/query")

    return render_template("form.html")