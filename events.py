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
    return True
