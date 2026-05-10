from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    abort
)

from flask_login import (
    login_required,
    current_user
)

from app.models import db, Query

admin = Blueprint('admin', __name__)


# ADMIN DASHBOARD
@admin.route("/admin")
@login_required
def admin_panel():

    # ADMIN CHECK
    if not current_user.is_admin:
        abort(403)

    rows = Query.query.order_by(
        Query.id.desc()
    ).all()

    total_queries = Query.query.count()

    pending_queries = Query.query.filter_by(
        status="Pending"
    ).count()

    return render_template(
        "admin.html",
        rows=rows,
        total_queries=total_queries,
        pending_queries=pending_queries
    )


# DELETE QUERY
@admin.route("/delete/<int:id>")
@login_required
def delete_query(id):

    if not current_user.is_admin:
        abort(403)

    query = Query.query.get(id)

    if query:

        db.session.delete(query)

        db.session.commit()

    return redirect(url_for("admin.admin_panel"))


# TOGGLE STATUS
@admin.route("/toggle-status/<int:id>")
@login_required
def toggle_status(id):

    if not current_user.is_admin:
        abort(403)

    query = Query.query.get(id)

    if query:

        if query.status == "Pending":
            query.status = "Resolved"

        else:
            query.status = "Pending"

        db.session.commit()

    return redirect(url_for("admin.admin_panel"))