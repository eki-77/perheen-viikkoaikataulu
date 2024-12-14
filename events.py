from flask import redirect, render_template, request, session, flash
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

from db import db
from app import app

def create_event(calendar_id, eventname, participants, day, start_time, end_time, items):
    sql = text("INSERT INTO events (calendar_id, day, start_time, end_time, eventname, items) VALUES (:calendar_id, :day, :start_time, :end_time, :eventname, :items) RETURNING id")
    result = db.session.execute(sql, {"calendar_id":calendar_id, "day":day, "start_time":start_time, "end_time":end_time, "eventname":eventname, "items":items})
    db.session.commit()
    event_id = result.fetchone()[0]
    for participant in participants:
        sql = text("INSERT INTO event_persons (event_id, person_id) VALUES (:event_id, :person_id)")
        db.session.execute(sql, {"event_id":event_id, "person_id":participant})
    db.session.commit()
    # Tähän pitäisi vielä lisätä try - except, joka palauttaisi False jos ei onnistunut tietokantaan kirjoitus
    return True

def get_event(id):
    sql = text("SELECT * FROM events WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    event = result.fetchone()
    if not event:
        return False
    return event

def get_weekday(day):
    days = ["", "Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
    on_days = ["", "Maanantaisin", "Tiistaisin", "Keskiviikkoisin", "Torstaisin", "Perjantaisin", "Lauantaisin", "Sunnuntaisin"]
    if 1 <= day <= 7:
        return [days[day], on_days[day]]
    else:
        return []
    