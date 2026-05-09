from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import db, User

auth = Blueprint("auth", __name__)


# REGISTER
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists")
            return redirect("/register")

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create new user
        new_user = User(
            username=username,
            password=hashed_password
        )

        # Save to database
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect("/login")

    return render_template("register.html")


# LOGIN
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Find user
        user = User.query.filter_by(username=username).first()

        # Check password
        if user and check_password_hash(user.password, password):

            login_user(user)

            flash("Login successful!")
            return redirect("/admin")

        flash("Invalid username or password")

    return render_template("login.html")


# LOGOUT
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully")
    return redirect("/login")