from app import app
from flask import redirect, render_template, request, session
from db import db
from sqlalchemy.sql import text

@app.route("/")
def index():
    result = db.session.execute(text("SELECT id, calendarname FROM calendars"))
    calendars_id_name = result.fetchall()
    return render_template("index.html", calendars=calendars_id_name)
    

