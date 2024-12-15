from flask import redirect, render_template, request, session, flash, abort
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

from db import db
from app import app
from access import has_access, is_admin, create_admin_if_missing
import person
import events
import calendars

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

@app.route("/error")
def error(message):
    return render_template("error.html")


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
            flash("Käyttäjätunnusta ei löydy.", 'error')
            return redirect("/login")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
                session["csrf_token"] = token_hex(16)
                return redirect("/")
            else:
                flash("Salasana on väärin.", 'error')
                return redirect("/login")
                
                
@app.route("/logout")
def logout():
    session.clear()
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
        session["csrf_token"] = token_hex(16)
        return redirect("/")

@app.route("/calendar/<int:id>")
def calendar(id):
    if not session:
        flash("Kirjaudu ensin sisään.", 'error')
        return redirect("/")
    if calendars.get_calendar(id) == False:
        flash("Aikataulua ei löydy", 'error')
        return redirect("/")
    if has_access(id) == False:
        flash("Sinulla ei ole oikeuksia katsoa tätä sivua. Oletko varmasti kirjautuneena sisään?", 'error')
        return redirect("/")
    sql = text("SELECT calendarname FROM calendars WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    a = result.fetchone()[0]
    session["cal_id"] = id
    sql = text("SELECT * FROM events WHERE calendar_id=:id")
    result = db.session.execute(sql, {"id":id})
    events_list = result.fetchall()
    person_list = person.get_persons(id)
    weekdays = [events.get_weekday(x)[0] for x in range(1, 8)]
    return render_template("calendar.html", id=id, name=a, events=events_list, persons=person_list, weekdays=weekdays)
    
@app.route("/calendar/create", methods=["GET", "POST"])
def calendar_create():
    if request.method == "GET":
        if not session:
            return render_template("error.html", message = "Kirjaudu ensin sisään.")
        return render_template("calendar_create.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        # If form returns calendar_id, this is an edit form
        if request.form["calendar_id"]:
            calendars.update_cal(request.form["calendar_id"], request.form["calendar_name"])
            return redirect("/")
        # Otherwise create new calendar
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

@app.route("/calendar/<int:id>/edit")
def calendar_edit(id):    
    if not session:
        flash("Kirjaudu ensin sisään.", 'error')
        return redirect("/")
    if has_access(id) == False:
        flash("Sinulla ei ole oikeuksia katsoa tätä sivua. Oletko varmasti kirjautuneena sisään?", 'error')
        return redirect("/")
    cal = calendars.get_calendar(id)
    if cal == False:
        flash("Tätä aikataulua ei ole olemassa.", 'error')
        return redirect("/")
    # Send calendar information to template to prefill the form and signify this is an edit, not create.
    return render_template("calendar_create.html", cal = cal)
    

@app.route("/calendar/<int:id>/person/create", methods=["GET", "POST"])
def person_create(id):
    if request.method == "GET":
        if not session:
            flash("Kirjaudu ensin sisään.", 'error')
            return redirect("/")
        if calendars.get_calendar(id) == False:
            flash("Aikataulua ei löydy", 'error')
            return redirect("/")
        if has_access(id) == False:
            return render_template("error.html", message = "Sinulla ei ole oikeuksia katsoa tätä sivua. Oletko varmasti kirjautuneena sisään?")
        return render_template("person_create.html", id = id)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        person_name = request.form["person_name"]
        sql = text("INSERT INTO persons (calendar_id, name) VALUES (:calendar_id, :person_name) RETURNING id")
        result = db.session.execute(sql, {"calendar_id":id, "person_name":person_name})
        db.session.commit()
        person_id = result.fetchone()[0]
        return redirect("/calendar/" + str(id))

@app.route("/calendar/<int:id>/event/create", methods=["GET", "POST"])
def event_create(id):
    if request.method == "GET":
        if not session:
            flash("Kirjaudu ensin sisään.", 'error')
            return redirect("/")
        if calendars.get_calendar(id) == False:
            flash("Aikataulua ei löydy", 'error')
            return redirect("/")
        if has_access(id) == False:
            flash("Sinulla ei ole oikeuksia katsoa tätä sivua. Oletko varmasti kirjautuneena sisään?", 'error')
            return redirect("/")
        person_list = person.get_persons(id)
        if person_list == []:
            flash("Aikataulullasi ei ole henkilöitä. Luo ensin henkilöt, joille haluat luoda tapahtumia.", 'error')
            return redirect("/calendar/" + str(id))
        return render_template("event_create.html", id=id, persons=person_list)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if request.form["start-time"] >= request.form["end-time"]:
            flash("Tapahtuman loppumisajan täytyy olla alkamisajan jälkeen.", 'error')
            return redirect("/calendar/" + str(id) + "/event/create")
        participants = request.form.getlist("participants")
        if participants == []:
            flash("Valitse tapahtumalle ainakin yksi osallistuja.", 'error')
            return redirect("/calendar/" + str(id) + "/event/create")
        result = events.create_event(id, request.form["event_name"], participants, request.form["weekday"], request.form["start-time"], request.form["end-time"], request.form["equipment"])
        # Tähän vielä tsekkaus, onnistuiko tietokantaan kirjoitus.
        return redirect("/calendar/" + str(id))

@app.route("/calendar/<int:id>/event/<int:event_id>")
def event(id, event_id):
    if not session:
        flash("Kirjaudu ensin sisään.", 'error')
        return redirect("/")
    if calendars.get_calendar(id) == False:
        flash("Aikataulua ei löydy", 'error')
        return redirect("/")
    if has_access(id) == False:
        flash("Sinulla ei ole oikeuksia katsoa tätä sivua. Oletko varmasti kirjautuneena sisään?", 'error')
        return redirect("/")
    event = events.get_event(event_id)
    if event == False:
        flash("Tapahtumaa ei löydy", 'error')
        return redirect("/calendar/" + str(id))
    persons = person.get_eventpersons(event_id)
    return render_template("event.html", event=event, cal_id=id, persons=persons, weekday=events.get_weekday(event[2])[1])
