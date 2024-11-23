from flask import Flask, render_template, request, redirect
import sqlite3

web = Flask(__name__)

def create_connection():
    conn = sqlite3.connect("survey.db")
    return conn

def create_table():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('''
CREATE TABLE IF NOT EXISTS survey_responses (
    si_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    rating TEXT NOT NULL CHECK (rating IN ('Excellent', 'Good', 'Average', 'Poor')),
    suggestions TEXT
)''')
    conn.commit()
    conn.close()

@web.route("/")
def home():
    return render_template("home.html")

@web.route("/about")
def about():
    return render_template("about.html")

@web.route("/menu")
def menu():
    return render_template("menu.html")

@web.route("/contact")
def contact():
    return render_template("contact.html")

@web.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        rating = request.form["rating"]
        suggestions = request.form["suggestions"]
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO survey_responses (name, email, rating, suggestions) VALUES (?, ?, ?, ?)",
                        (name, email, rating, suggestions))
            conn.commit()
        except sqlite3.IntegrityError as e:
            return f"Error: {e}" 
        finally:
            conn.close()
        return redirect("/")
    return render_template("survey.html")


if __name__ == "__main__":
    create_table()
    web.run(debug = True)
