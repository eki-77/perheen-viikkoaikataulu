from app import app
from flask import redirect, render_template, request, session
from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    result = db.session.execute(text("SELECT id, calendarname FROM calendars"))
    calendars_id_name = result.fetchall()
    return render_template("index.html", calendars=calendars_id_name)

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()    
        if not user:
            # TODO: invalid username
            pass
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
                return redirect("/")
            else:
                # TODO: invalid password
                pass
                

            

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("create_user.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = False
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)")
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
        db.session.commit()
        session["username"] = username
        return redirect("/")

@app.route("/calendar/<int:id>")
def calendar(id):
    sql = text("SELECT calendarname FROM calendars WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    a = result.fetchone()[0]
    sql = text("SELECT * FROM events WHERE calendar_id=:id")
    result = db.session.execute(sql, {"id":id})
    events = result.fetchall()
    return render_template("calendar.html", id=id, name=a, events=events)
    
