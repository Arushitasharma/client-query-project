from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.models import db, User

import re

auth = Blueprint('auth', __name__)


# REGISTER
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username").strip().lower()

        password = request.form.get("password").strip()

        # USERNAME SPACES CHECK
        if " " in username:

            flash("Username cannot contain spaces")

            return redirect("/register")

        # USERNAME LENGTH CHECK
        if len(username) < 4 or len(username) > 15:

            flash("Username must be between 4 and 15 characters")

            return redirect("/register")

        # PASSWORD LENGTH CHECK
        if len(password) < 4 or len(password) > 15:

            flash("Password must be between 4 and 15 characters")

            return redirect("/register")

        # PASSWORD REGEX CHECK
        password_pattern = (
            r"^(?=.*[a-z])"
            r"(?=.*[A-Z])"
            r"(?=.*\d)"
            r"(?=.*[@$!%*?&])"
            r".{4,15}$"
        )

        if not re.match(password_pattern, password):

            flash(
                "Password must contain uppercase, lowercase, digit and special character"
            )

            return redirect("/register")

        # CHECK EXISTING USER
        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            flash("Username already exists")

            return redirect("/register")

        # DEFAULT USERS ARE NOT USERS
        is_admin = False

        # HASH PASSWORD
        hashed_password = generate_password_hash(password)

        # CREATE USER
        new_user = User(
            username=username,
            password=hashed_password,
            is_admin=is_admin
        )

        try:

            db.session.add(new_user)

            db.session.commit()

            flash("Registration successful")

            return redirect("/login")

        except Exception:

            flash("Something went wrong")

            return redirect("/register")

    return render_template("register.html")


# LOGIN
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username").strip().lower()

        password = request.form.get("password").strip()

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            flash("Login successful")

            return redirect("/")

        else:

            flash("Invalid username or password")

            return redirect("/login")

    return render_template("login.html")


# LOGOUT
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully")

    return redirect("/login")