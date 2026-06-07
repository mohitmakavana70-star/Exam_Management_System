from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

# 🔐 Password security
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret"

def get_db():
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row

    try:
        db.execute("ALTER TABLE users ADD COLUMN attempted INTEGER DEFAULT 0")
    except:
        pass

    db.execute("UPDATE users SET attempted=0 WHERE attempted IS NULL")
    db.commit()

    return db

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET","POST"])
def signup():
    msg = ""

    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        cpwd = request.form["confirm_password"]

        if pwd != cpwd:
            msg = "Passwords do not match!"
            return render_template("signup.html", msg=msg)

        db = get_db()

        existing = db.execute("SELECT * FROM users WHERE username=?", (user,)).fetchone()

        if existing:
            msg = "User already exists!"
            return render_template("signup.html", msg=msg)

        hashed_pwd = generate_password_hash(pwd)

        db.execute(
            "INSERT INTO users (username,password,attempted) VALUES (?,?,0)",
            (user, hashed_pwd)
        )
        db.commit()

        return redirect("/")

    return render_template("signup.html", msg=msg)

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET","POST"])
def login():
    msg = ""

    session.clear()

    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        # ADMIN LOGIN
        if user == "admin" and pwd == "admin@888":
            session["admin"] = True
            return redirect("/admin")

        db = get_db()

        user_data = db.execute(
            "SELECT * FROM users WHERE username=?",
            (user,)
        ).fetchone()

        if user_data and check_password_hash(user_data["password"], pwd):

            if user_data["attempted"] == 1:
                return render_template("blocked.html")

            session["user"] = user
            return redirect("/exam")

        else:
            msg = "Invalid username or password!"

    return render_template("login.html", msg=msg)

# ---------------- EXAM ----------------
@app.route("/exam", methods=["GET","POST"])
def exam():
    if "user" not in session:
        return redirect("/")

    db = get_db()

    user_data = db.execute(
        "SELECT * FROM users WHERE username=?",
        (session["user"],)
    ).fetchone()

    if user_data["attempted"] == 1:
        return "You already attempted or violated exam!"

    if request.method == "POST":
        questions = db.execute("SELECT * FROM questions").fetchall()
        score = 0

        for q in questions:
            if request.form.get(str(q["id"])) == q["correct"]:
                score += 1

        db.execute(
            "UPDATE users SET attempted=1 WHERE username=?",
            (session["user"],)
        )

        db.execute(
            "INSERT INTO scores VALUES (NULL,?,?)",
            (session["user"], score)
        )

        db.commit()
        session.clear()
        return redirect("/")

    questions = db.execute("SELECT * FROM questions").fetchall()
    return render_template("exam.html", questions=questions)

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/")

    db = get_db()
    scores = db.execute("SELECT * FROM scores").fetchall()

    return render_template("admin.html", scores=scores)

# ---------------- ADD QUESTIONS ----------------
@app.route("/add_questions", methods=["GET","POST"])
def add_questions():
    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":
        db = get_db()

        db.execute("DELETE FROM questions")

        # 🔥 UNBLOCK ALL USERS
        db.execute("UPDATE users SET attempted=0")

        for i in range(1,11):
            q = request.form.get(f"q{i}")
            a = request.form.get(f"a{i}")
            b = request.form.get(f"b{i}")
            c = request.form.get(f"c{i}")
            d = request.form.get(f"d{i}")
            ans = request.form.get(f"ans{i}")

            if q:
                db.execute("""
                INSERT INTO questions 
                (question,option_a,option_b,option_c,option_d,correct)
                VALUES (?,?,?,?,?,?)
                """,(q,a,b,c,d,ans))

        db.commit()

    return render_template("add_questions.html")

# ---------------- VIEW SCORES ----------------
@app.route("/view_scores")
def view_scores():
    if "admin" not in session:
        return redirect("/")

    db = get_db()
    data = db.execute("SELECT * FROM scores").fetchall()
    return render_template("view_scores.html", data=data)

# ---------------- DELETE USERS ----------------
@app.route("/delete_users")
def delete_users():
    if "admin" not in session:
        return redirect("/")

    db = get_db()
    db.execute("DELETE FROM users")
    db.commit()

    return "All users deleted!"

# ---------------- VIOLATION ----------------
@app.route("/violation", methods=["POST"])
def violation():
    if "user" not in session:
        return "Not logged in"

    db = get_db()

    questions = db.execute("SELECT * FROM questions").fetchall()
    score = 0

    for q in questions:
        ans = request.form.get(str(q["id"]))
        if ans == q["correct"]:
            score += 1

    db.execute("UPDATE users SET attempted=1 WHERE username=?", (session["user"],))

    db.execute("INSERT INTO scores VALUES (NULL,?,?)",(session["user"],score))

    db.commit()

    return "Blocked"

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RESET ----------------
@app.route("/reset")
def reset():
    if "admin" not in session:
        return redirect("/")

    db = get_db()
    db.execute("DELETE FROM questions")
    db.execute("DELETE FROM scores")
    db.commit()
    return "All Data Reset!"

# 🔥 FINAL RUN (IMPORTANT FOR RENDER)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)