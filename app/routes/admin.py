from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

from app.database import get_db

admin = Blueprint('admin', __name__)


# ADMIN PAGE
@admin.route("/admin")
@login_required
def admin_panel():

    search = request.args.get("search", "")

    conn = get_db()
    cursor = conn.cursor()

    if search:

        cursor.execute(
            """
            SELECT * FROM queries
            WHERE name LIKE ?
            OR email LIKE ?
            ORDER BY id DESC
            """,
            (f"%{search}%", f"%{search}%")
        )

    else:

        cursor.execute(
            "SELECT * FROM queries ORDER BY id DESC"
        )

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        rows=rows,
        search=search
    )


# DELETE QUERY
@admin.route("/delete/<int:id>")
@login_required
def delete_query(id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM queries WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin.admin_panel"))


# TOGGLE STATUS
@admin.route("/toggle-status/<int:id>")
@login_required
def toggle_status(id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM queries WHERE id = ?",
        (id,)
    )

    current_status = cursor.fetchone()[0]

    if current_status == "Pending":
        new_status = "Resolved"
    else:
        new_status = "Pending"

    cursor.execute(
        "UPDATE queries SET status = ? WHERE id = ?",
        (new_status, id)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin.admin_panel"))