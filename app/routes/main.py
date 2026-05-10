from flask import Blueprint, render_template, request, redirect, flash
from app.models import db, Query

main = Blueprint('main', __name__)


# HOME PAGE
@main.route("/")
def home():
    return render_template("form.html")


# SUBMIT QUERY
@main.route("/submit", methods=["POST"])
def submit_query():

    name = request.form.get("name")
    email = request.form.get("email")
    query_text = request.form.get("query")

    new_query = Query(
        name=name,
        email=email,
        query=query_text
    )

    db.session.add(new_query)
    db.session.commit()

    flash("Query submitted successfully!")

    return redirect("/")