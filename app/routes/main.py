from flask import Blueprint, render_template, request, redirect
from app.database import get_db

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("form.html")


@main.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    query = request.form["query"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO queries (name, email, query, status) VALUES (?, ?, ?, ?)",
        (name, email, query, "Open")
    )

    conn.commit()
    conn.close()

    # 👉 automatic redirect after submit
    return redirect("/admin")