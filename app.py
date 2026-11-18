"""
Flask application – IIPS-MCA Alumni Management System
Modules: Alumni Registration, Employment Tracking, Mentorship, Analytics
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection, init_db
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = "alumni_secret_key_2024"

# ──────────────────────────────────────────────────────────
# HOME
# ──────────────────────────────────────────────────────────
@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT COUNT(*) AS total FROM alumni")
    total_alumni = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM employment WHERE end_year IS NULL")
    employed = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM mentorship")
    mentors = cur.fetchone()["total"]
    cur.execute("""
        SELECT batch_year, COUNT(*) AS count
        FROM alumni
        WHERE batch_year IS NOT NULL
        GROUP BY batch_year ORDER BY batch_year DESC LIMIT 6
    """)
    batch_stats = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html",
                           total_alumni=total_alumni,
                           employed=employed,
                           mentors=mentors,
                           batch_stats=batch_stats)

# ──────────────────────────────────────────────────────────
# ALUMNI REGISTRATION
# ──────────────────────────────────────────────────────────
@app.route("/alumni")
def list_alumni():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM alumni ORDER BY created_at DESC")
    alumni = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("alumni_list.html", alumni=alumni)


@app.route("/alumni/add", methods=["GET", "POST"])
def add_alumni():
    if request.method == "POST":
        name       = request.form["name"]
        email      = request.form["email"]
        phone      = request.form.get("phone", "")
        batch_year = request.form.get("batch_year") or None
        course     = request.form.get("course", "MCA")
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO alumni (name, email, phone, batch_year, course) VALUES (%s,%s,%s,%s,%s)",
                (name, email, phone, batch_year, course)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Alumni registered successfully!", "success")
            return redirect(url_for("list_alumni"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template("alumni_form.html", action="Add", alumni=None)


@app.route("/alumni/edit/<int:alumni_id>", methods=["GET", "POST"])
def edit_alumni(alumni_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == "POST":
        name       = request.form["name"]
        email      = request.form["email"]
        phone      = request.form.get("phone", "")
        batch_year = request.form.get("batch_year") or None
        course     = request.form.get("course", "MCA")
        cur.execute(
            "UPDATE alumni SET name=%s, email=%s, phone=%s, batch_year=%s, course=%s WHERE id=%s",
            (name, email, phone, batch_year, course, alumni_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("Alumni updated!", "success")
        return redirect(url_for("list_alumni"))
    cur.execute("SELECT * FROM alumni WHERE id=%s", (alumni_id,))
    alumni = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("alumni_form.html", action="Edit", alumni=alumni)


@app.route("/alumni/delete/<int:alumni_id>")
def delete_alumni(alumni_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM alumni WHERE id=%s", (alumni_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Alumni removed.", "warning")
    return redirect(url_for("list_alumni"))

# ──────────────────────────────────────────────────────────
# EMPLOYMENT TRACKING
# ──────────────────────────────────────────────────────────
@app.route("/employment")
def list_employment():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT e.*, a.name AS alumni_name
        FROM employment e
        JOIN alumni a ON a.id = e.alumni_id
        ORDER BY e.created_at DESC
    """)
    records = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("employment_list.html", records=records)


@app.route("/employment/add", methods=["GET", "POST"])
def add_employment():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == "POST":
        alumni_id   = request.form["alumni_id"]
        company     = request.form["company"]
        designation = request.form["designation"]
        city        = request.form.get("city", "")
        start_year  = request.form.get("start_year") or None
        end_year    = request.form.get("end_year") or None
        cur.execute(
            "INSERT INTO employment (alumni_id, company, designation, city, start_year, end_year) VALUES (%s,%s,%s,%s,%s,%s)",
            (alumni_id, company, designation, city, start_year, end_year)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("Employment record added!", "success")
        return redirect(url_for("list_employment"))
    cur.execute("SELECT id, name FROM alumni ORDER BY name")
    alumni_list = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("employment_form.html", alumni_list=alumni_list, record=None)


@app.route("/employment/delete/<int:rec_id>")
def delete_employment(rec_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employment WHERE id=%s", (rec_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Record deleted.", "warning")
    return redirect(url_for("list_employment"))

# ──────────────────────────────────────────────────────────
# MENTORSHIP
# ──────────────────────────────────────────────────────────
@app.route("/mentorship")
def list_mentorship():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT m.*, a.name AS mentor_name
        FROM mentorship m
        JOIN alumni a ON a.id = m.mentor_id
        ORDER BY m.created_at DESC
    """)
    records = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("mentorship_list.html", records=records)


@app.route("/mentorship/add", methods=["GET", "POST"])
def add_mentorship():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == "POST":
        mentor_id    = request.form["mentor_id"]
        topic        = request.form["topic"]
        availability = request.form.get("availability", "")
        cur.execute(
            "INSERT INTO mentorship (mentor_id, topic, availability) VALUES (%s,%s,%s)",
            (mentor_id, topic, availability)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("Mentorship slot added!", "success")
        return redirect(url_for("list_mentorship"))
    cur.execute("SELECT id, name FROM alumni ORDER BY name")
    alumni_list = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("mentorship_form.html", alumni_list=alumni_list)


@app.route("/mentorship/delete/<int:rec_id>")
def delete_mentorship(rec_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM mentorship WHERE id=%s", (rec_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Mentorship record removed.", "warning")
    return redirect(url_for("list_mentorship"))

# ──────────────────────────────────────────────────────────
# ANALYTICS
# ──────────────────────────────────────────────────────────
@app.route("/analytics")
def analytics():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # Top companies
    cur.execute("""
        SELECT company, COUNT(*) AS count
        FROM employment GROUP BY company ORDER BY count DESC LIMIT 5
    """)
    top_companies = cur.fetchall()
    # Placement % by batch
    cur.execute("""
        SELECT a.batch_year,
               COUNT(DISTINCT a.id) AS total,
               COUNT(DISTINCT e.alumni_id) AS placed
        FROM alumni a
        LEFT JOIN employment e ON e.alumni_id = a.id AND e.end_year IS NULL
        WHERE a.batch_year IS NOT NULL
        GROUP BY a.batch_year ORDER BY a.batch_year DESC LIMIT 6
    """)
    placement_stats = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("analytics.html",
                           top_companies=top_companies,
                           placement_stats=placement_stats)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
