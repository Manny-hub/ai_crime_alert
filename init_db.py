import sqlite3
import os

DB_PATH = os.path.join("instance", "app.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop old alerts table
cursor.execute("DROP TABLE IF EXISTS alerts")

# Recreate alerts table
cursor.execute("""
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    incident_date TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("Alerts table recreated successfully.")
