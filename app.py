from flask import Flask,render_template,request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
import psycopg2

app = Flask(__name__,template_folder = 'templates')

def db_connect():
    conn = psycopg2.connect(host="localhost", database="yafsDB", user="postgres", password="Mikey6972")
    
    return conn

@app.route ('/')
def index():
    """Shows index/homepage"""
    return render_template("index.html")

@app.route ('/admin')
def admin():
    """Shows admin page"""
    return render_template("admin.html")

@app.route ('/users')
def user_query():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM users;''')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("users.html", users=users)

@app.route ('/feedback', methods = ["GET","POST"])
def feedback():
        username = request.form.get("username")
        public = request.form.get("public")
        contact = request.form.get("contact")
        feedback_desc = request.form.get("feedback_desc")
        email = request.form.get("email")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (id, username, contact, email, feedback_desc, created_at, is_public) VALUES (DEFAULT,%s,%s,%s,%s,%s,%s)", (username,contact,email,feedback_desc,timestamp,public)
            )
        conn.commit()

        return render_template("feedback.html")
            

if __name__=="__main__":
    app.run()
    