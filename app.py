from flask import Flask, render_template, redirect, url_for, request, flash, session
import os
import sqlite3
import feedparser
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # change to env var in production

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

# -------------------
# NEWS FETCHER
# -------------------
import feedparser

NEWS_FEEDS = {
    "ai_general": "https://news.google.com/rss/search?q=artificial+intelligence",
    "ai_ethics": "https://news.google.com/rss/search?q=ai+ethics",
    "ai_security": "https://news.google.com/rss/search?q=ai+cybersecurity",
    "ai_business": "https://news.google.com/rss/search?q=ai+business",
    "ai_research": "https://news.google.com/rss/search?q=ai+research",
    "ai_crime": "https://news.google.com/rss/search?q=AI+crime+OR+artificial+intelligence+crime&hl=en-US&gl=US&ceid=US:en"
}

def get_news():
    feed = feedparser.parse(NEWS_FEEDS["ai_crime"])
    news_items = []
    for entry in feed.entries[:15]:
        # Some feeds contain richer content under "content"
        content = ""
        if hasattr(entry, "content"):
            content = entry.content[0].value
        elif hasattr(entry, "summary"):
            content = entry.summary

        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "published": getattr(entry, "published", ""),
            "summary": content,
        })
   # Shuffle so the items don’t look static
    random.shuffle(news_items)
    return news_items[:20]  # return top 20 mixed results

# -------------------
# ROUTES
# -------------------

@app.route('/')
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        # Simple demo auth
        if username == "admin" and password == "admin123":
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    prediction = None
    if request.method == "POST":
        text = request.form.get("text", "")
        if text:
            # 🔹 Replace this with real AI detection model later
            prediction = "AI-generated" if "AI" in text else "Human-written"

    total_alerts = get_total_alerts()
    news_preview = get_news()[:3]

    return render_template("dashboard.html",
                           user=session["user"],
                           total_alerts=total_alerts,
                           news_preview=news_preview,
                           prediction=prediction)


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

    items = get_news()

    # Store each news item in alerts table (if not already stored)
    with db() as conn:
        for item in items:
            exists = conn.execute(
                "SELECT 1 FROM alerts WHERE title = ? AND incident_date = ?",
                (item['title'], item['published'])
            ).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO alerts (title, category, location, description, incident_date) VALUES (?, ?, ?, ?, ?)",
                    (item['title'], 'News', 'Online', item['summary'] or item['title'], item['published'])
                )
        conn.commit()

    return render_template("news.html", items=items)

# -------------------
# USERS (Dummy)
# -------------------
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


@app.route("/api/news")
def api_news():
    items = get_news()
    return jsonify(items)

if __name__ == "__main__":
    app.run(debug=True)
