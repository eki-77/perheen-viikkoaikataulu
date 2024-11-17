from app import app
from flask import redirect, render_template, request, session
from db import db
from sqlalchemy.sql import text

@app.route("/")
def index():
    result = db.session.execute(text("SELECT id, calendarname FROM calendars"))
    calendars_id_name = result.fetchall()
    return render_template("index.html", calendars=calendars_id_name)

@app.route("/calendar/<int:id>")
def calendar(id):
    sql = text("SELECT calendarname FROM calendars WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    a = result.fetchone()[0]
    sql = text("SELECT * FROM events WHERE calendar_id=:id")
    result = db.session.execute(sql, {"id":id})
    events = result.fetchall()
    return render_template("calendar.html", id=id, name=a, events=events)
    

