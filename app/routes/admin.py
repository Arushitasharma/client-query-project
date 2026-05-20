from flask import (
    Blueprint,
    render_template,
    redirect,
    flash,
    abort
)

from flask_login import (
    login_required,
    current_user
)

from app.models import db, Query


admin = Blueprint("admin", __name__)


# ADMIN DASHBOARD
@admin.route("/admin")
@login_required
def admin_dashboard():

    # BLOCK NON-ADMINS
    if not current_user.is_admin:

        abort(403)

    # FETCH ALL QUERIES
    rows = Query.query.order_by(
        Query.id.desc()
    ).all()

    # STATS
    total_queries = Query.query.count()

    pending_queries = Query.query.filter_by(
        status="Pending"
    ).count()

    resolved_queries = Query.query.filter_by(
        status="Resolved"
    ).count()

    return render_template(

        "admin/admin.html",

        rows=rows,

        total_queries=total_queries,

        pending_queries=pending_queries,

        resolved_queries=resolved_queries
    )


# TOGGLE STATUS
@admin.route("/toggle-status/<int:id>")
@login_required
def toggle_status(id):

    # BLOCK NON-ADMINS
    if not current_user.is_admin:

        abort(403)

    query = Query.query.get_or_404(id)

    if query.status == "Pending":

        query.status = "Resolved"

    else:

        query.status = "Pending"

    db.session.commit()

    flash("Query status updated")

    return redirect("/admin")


# DELETE QUERY
@admin.route("/delete/<int:id>")
@login_required
def delete_query(id):

    # BLOCK NON-ADMINS
    if not current_user.is_admin:

        abort(403)

    query = Query.query.get_or_404(id)

    db.session.delete(query)

    db.session.commit()

    flash("Query deleted successfully")

    return redirect("/admin")

@admin.route("/make-admin/<username>")
def make_admin(username):

    user = User.query.filter_by(
        username=username.lower()
    ).first()

    if not user:

        return "User not found"

    user.is_admin = True

    db.session.commit()

    return f"{username} is now admin"