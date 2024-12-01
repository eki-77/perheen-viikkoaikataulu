from app import app
from flask import redirect, render_template, request, session
from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def has_access(calendar_id):
    if is_admin():
        return True
    if not session:
        return False
    username = session["username"]
    sql = text("SELECT CO.user_id FROM calendar_owners CO, users U WHERE U.username=:username AND U.id = CO.user_id AND CO.calendar_id=:calendar_id")
    result = db.session.execute(sql, {"username":username, "calendar_id":calendar_id})
    rights = result.fetchone()
    if rights:
        return True
    else:
        return False
    
def is_admin():
    if not session:
        return False
    #print(session)
    #print(session["username"])
    username = session["username"]
    sql = text("SELECT admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    #print("admintesti, userin admintieto", user.admin)
    return user.admin

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
    if session:
        session.pop("cal_id", default=None)
        if is_admin():
            result = db.session.execute(text("SELECT id, calendarname FROM calendars"))
        else:
            username = session["username"]
            sql = text("SELECT C.id, C.calendarname FROM calendars C, calendar_owners CO, users U WHERE U.username=:username AND U.id = CO.user_id AND CO.calendar_id = C.id")
            result = db.session.execute(sql, {"username":username})
        calendars_id_name = result.fetchall()
        return render_template("index.html", calendars=calendars_id_name)
    return render_template("index.html", calendars=[])

#@app.route("/error")
#def error(message):
#    return render_template("error.html")


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
            return render_template("error.html", message = "Käyttäjätunnusta ei löydy.")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
                session["csrf_token"] = token_hex(16)
                return redirect("/")
            else:
                return render_template("error.html", message = "Salasana on väärin.")
                
                
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
    if has_access(id) == False:
        return render_template("error.html", message = "Sinulla ei ole oikeuksia katsoa tätä sivua. Oletko varmasti kirjautuneena sisään?")
    sql = text("SELECT calendarname FROM calendars WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    a = result.fetchone()[0]
    session["cal_id"] = id
    sql = text("SELECT * FROM events WHERE calendar_id=:id")
    result = db.session.execute(sql, {"id":id})
    events = result.fetchall()
    sql = text("SELECT * FROM persons WHERE calendar_id=:id")
    result = db.session.execute(sql, {"id":id})
    persons = result.fetchall()
    return render_template("calendar.html", id=id, name=a, events=events, persons=persons)
    
@app.route("/calendar/create", methods=["GET", "POST"])
def calendar_create():
    if request.method == "GET":
        if not session:
            return render_template("error.html", message = "Kirjaudu ensin sisään.")
        return render_template("calendar_create.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        calendar_name = request.form["calendar_name"]
        sql = text("INSERT INTO calendars (calendarname) VALUES (:calendar_name) RETURNING id")
        result = db.session.execute(sql, {"calendar_name":calendar_name})
        db.session.commit()
        cal_id = result.fetchone()[0]
        sql = text("SELECT id FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":session["username"]})
        user_id = result.fetchone()[0]
        sql = text("INSERT INTO calendar_owners (calendar_id, user_id) VALUES (:calendar_id, :user_id)")
        db.session.execute(sql, {"calendar_id":cal_id, "user_id":user_id})
        db.session.commit()
        return redirect("/")