from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.models import db, Query

main = Blueprint('main', __name__)


@main.route("/")
def index():

    if not current_user.is_authenticated:
        return redirect("/login")

    return redirect("/dashboard")

@main.route("/dashboard")
@login_required
def dashboard():

    user_queries = Query.query.filter_by(
            user_id=current_user.id
        ).order_by(
            Query.id.desc()
        ).all()

    return render_template("dashboard/dashboard.html", queries=user_queries)

@main.route("/create-query")
@login_required
def create_query():
    return render_template("dashboard/create_query.html")

# SUBMIT QUERY
@main.route("/submit", methods=["POST"])
@login_required
def submit_query():

    title = request.form.get("title")

    query_text = request.form.get("query")

    new_query = Query(
        title=title,
        message=query_text,
        user_id=current_user.id
    )

    db.session.add(new_query)

    db.session.commit()

    flash("Query submitted successfully!")

    return redirect("/dashboard")