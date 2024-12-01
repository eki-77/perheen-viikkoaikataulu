from app import app
from flask import redirect, render_template, request, session
from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def has_access(user, page):
    # TODO: function to check if user is allowed to access page
    return True

def is_admin():
    if not session:
        return False
    print(session)
    #print(session["username"])
    #print("admintesti", un)
    #sql = text("SELECT admin FROM users WHERE username=:username")
    #result = db.session.execute(sql, {"username":username})
    #user = result.fetchone()
    #print("admintesti, userin admintieto", user.admin)
    #return user.admin



def create_admin_if_missing():
    sql = text("SELECT 1 FROM users WHERE username=:admin")
    result = db.session.execute(sql, {"admin":"admin"})
    if not result.fetchone():
        print("ei adminia!")
        hash_value = generate_password_hash("tsoha-admin")
        sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)")
        db.session.execute(sql, {"username":"admin", "password":hash_value, "admin":True})
        db.session.commit()
    else:
        print("löytyi admin")

@app.route("/")
def index():
    create_admin_if_missing()
    if is_admin():
        result = db.session.execute(text("SELECT id, calendarname FROM calendars"))
        calendars_id_name = result.fetchall()
        return render_template("index.html", calendars=calendars_id_name)
    else:
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
                session["csrf_token"] = token_hex(16)
                return redirect("/")
            else:
                # TODO: invalid password
                pass
                
@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("create_user.html")
    if request.method == "POST":
        #if session["csrf_token"] != request.form["csrf_token"]:
        #    abort(403)
        username = request.form["username"]
        password = request.form["password"]
        admin = False
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)")
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
        db.session.commit()
        session["username"] = username
        session["csrf_token"] = token_hex(16)
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
    
