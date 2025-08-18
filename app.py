from flask import Flask, render_template, redirect, url_for, request, flash, session
import os
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect", methods=["GET", "POST"])
def detect():
    prediction = None
    if request.method == "POST":
        text = request.form["text"]
        # your AI detection logic
        prediction = "AI-generated"  # dummy example
    return render_template("detect.html", prediction=prediction)

app = Flask(__name__)
app.secret_key = "supersecretkey"  # change to env var in production

import feedparser

NEWS_FEEDS = {
    "crime": "https://news.google.com/rss/search?q=crime&hl=en-US&gl=US&ceid=US:en"
}

def get_news():
    feed = feedparser.parse(NEWS_FEEDS["crime"])
    news_items = []
    for entry in feed.entries[:10]:  # latest 10
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })
    return news_items



# Home redirects to login if not authenticated
@app.route('/')
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        # Simple demo auth (replace with DB later)
        if username == "admin" and password == "admin123":
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")


#dashboard route:
@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    total_alerts = get_total_alerts() if 'get_total_alerts' in globals() else 0
    return render_template("dashboard.html", user=session["user"], total_alerts=total_alerts)

# Logout
@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))

# Report submission page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Handle file upload
        pass
    return render_template("upload.html")

# Database setup
DB_PATH = os.path.join("instance", "app.db")


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_total_alerts():
    with db() as conn:
        cur = conn.execute("SELECT COUNT(*) AS c FROM alerts")
        return cur.fetchone()["c"]


# Dummy user list
users = [
    {"id": 1, "name": "Alice Doe", "email": "alice@example.com"},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com"}
]

@app.route("/manage_users")
def manage_users():
    return render_template("manage_users.html", users=users)

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return redirect(url_for("manage_users"))

@app.route('/report', methods=['GET', 'POST'])
def report_crime():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == 'POST':
        title = request.form.get('title','').strip()
        category = request.form.get('category','').strip()
        location = request.form.get('location','').strip()
        description = request.form.get('description','').strip()
        incident_date = request.form.get('incident_date','').strip()

        if not all([title, category, location, description, incident_date]):
            flash("All fields are required.", "warning")
            return redirect(url_for('report_crime'))

        with db() as conn:
            conn.execute("""
                INSERT INTO alerts (title, category, location, description, incident_date)
                VALUES (?, ?, ?, ?, ?)
            """, (title, category, location, description, incident_date))
            conn.commit()

        flash("Incident reported successfully.", "success")
        return redirect(url_for('alerts'))

    return render_template('report.html')

@app.route('/alerts')
def alerts():
    if "user" not in session:
        return redirect(url_for("login"))
    q = request.args.get('q','').strip()
    cat = request.args.get('cat','').strip()

    sql = "SELECT * FROM alerts WHERE 1=1"
    params = []
    if q:
        sql += " AND (title LIKE ? OR location LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    if cat:
        sql += " AND category = ?"
        params.append(cat)
    sql += " ORDER BY created_at DESC"

    with db() as conn:
        rows = conn.execute(sql, params).fetchall()

    return render_template('alerts.html', alerts=rows, q=q, cat=cat)

@app.route("/news")
def news():
    if "user" not in session:
        return redirect(url_for("login"))

    items = get_news()  # fetch latest 10 news

    # Store each news item in alerts table (if not already stored)
    with db() as conn:
        for item in items:
            # Check if this news is already in alerts
            exists = conn.execute(
                "SELECT 1 FROM alerts WHERE title = ? AND incident_date = ?",
                (item['title'], item['published'])
            ).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO alerts (title, category, location, description, incident_date) VALUES (?, ?, ?, ?, ?)",
                    (item['title'], 'News', 'Online', item['title'], item['published'])
                )
        conn.commit()

    return render_template("news.html", items=items)




if __name__ == "__main__":
    app.run(debug=True)

