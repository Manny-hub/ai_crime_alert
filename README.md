


# AI Crime Alert System

An AI-powered surveillance and alert system focused on ethical crime detection, cybersecurity, and public accountability—built as a final-year project to explore responsible AI deployment in public safety.

---

##  Features

- **Surveillance Alerts**  
  Submit and view crime incidents via an intuitive web interface with real-time alert capabilities.

- **Secure Data Handling**  
  Utilizes SQLite with encryption support for incident data and audit logs.

- **User Management**  
  Admin portal for managing user access, deleting users, and monitoring system usage.

- **News Integration**  
  Fetches and displays relevant *AI and crime-related news* using RSS feeds and Feedparser in Python.

- **Accountability Focus**  
  Keeps detailed logs of crime submissions and system activity, enabling transparency.

---

````markdown

##  Project Structure

```text
├── app.py                # Main Flask application with routing & logic
├── init_db.py            # Script to initialize SQLite database and tables
├── schema.sql            # SQL schema for setting up the database
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates (login, dashboard, report, alerts, news)
├── static/               # Static assets (CSS, JS)
└── README.md             # This document
````

---

## Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite
* **Frontend:** HTML, CSS (Bootstrap), JavaScript
* **News Fetching:** Python + Feedparser
* **Security:** Session-based authentication, password hashing, audit logs

---

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Manny-hub/ai_crime_alert.git
   cd ai_crime_alert
   ```

2. **Create a Python virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**

   ```bash
   python init_db.py
   ```

5. **Run the application**

   ```bash
   flask run
   ```

   Access the app at `http://127.0.0.1:5000`

---

## Usage

* Navigate to the **Login** page and sign in (default credentials if implemented).
* **Submit an Incident/Alert** via the Report page.
* **View submitted alerts** on the Alerts page.
* **Visit the News page** to view curated AI-crime news.
* Explore the **Dashboard** to manage alerts, users, and see high-level stats.


## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.



```

Let me know if you'd like **code snippets**, screenshots, or badges (e.g., dependencies, license) added, or if you’d like this adapted for a more academic or developer audience.
::contentReference[oaicite:0]{index=0}
```
