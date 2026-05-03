from flask import Blueprint, render_template, request, redirect, session

# THIS LINE WAS MISSING ❗
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        if user == "admin" and password == "admin":
            session["user"] = user
            return redirect("/admin")

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")