from flask import Blueprint, render_template, redirect, url_for
from app.database import get_db

admin = Blueprint('admin', __name__)

# ADMIN PAGE
@admin.route("/admin")
def admin_panel():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM queries ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    return render_template("admin.html", rows=rows)


# DELETE QUERY
@admin.route("/delete/<int:id>")
def delete_query(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM queries WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin.admin_panel"))