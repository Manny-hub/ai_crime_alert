Sure! Here's your README content with **steps 1 to 6 fully included** under Installation & Setup:

````markdown
# AI Crime Alerts & Detection System

A Flask-based web application that allows users to:  
- Detect whether text is AI-generated.  
- Submit crime incident reports.  
- Fetch the latest online crime news and store it as alerts.  

---

## Features

1. **User Authentication**
   - Login with a username and password.
   - Protected routes for authorized users only.
   - Logout functionality.

2. **Crime Alerts**
   - Users can report crimes via a form.
   - All reports are stored in a SQLite database.
   - Dashboard shows total alerts and user info.

3. **Latest News Fetching**
   - Fetch latest crime news using RSS feed (`feedparser`).
   - Automatically store news as alerts in the database.
   - Display news on a dedicated page.

4. **User Management** (Demo)
   - View and delete users (for demo purposes).

---

## Technology Stack

- **Backend**: Python, Flask  
- **Database**: SQLite  
- **Templating**: Jinja2  
- **Web Scraping / RSS**: feedparser  
- **Frontend**: HTML, CSS (Bootstrap optional)  

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Manny-hub/ai_crime_alert.git
cd ai_crime_alert
````

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv       # Create virtual environment
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

```bash
python create_db.py
```

This will create the `instance/app.db` SQLite database with the necessary tables (`detections` and `alerts`).

### 5. Run the Flask App

Set environment variables and start the Flask development server:

**Linux/macOS**

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

**Windows (CMD)**

```cmd
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### 6. Login Credentials (Demo)

* **Username:** admin
* **Password:** admin123

```
