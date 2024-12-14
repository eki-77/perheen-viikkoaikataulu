from flask import redirect, render_template, request, session, flash
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

from db import db
from app import app

def get_persons(id):
    sql = text("SELECT * FROM persons WHERE calendar_id=:id")
    result = db.session.execute(sql, {"id":id})
    persons = result.fetchall()
    return persons

def get_eventpersons(event_id):
    sql = text("SELECT P.name, P.id FROM persons P, event_persons EP WHERE P.id = EP.person_id AND EP.event_id=:id")
    result = db.session.execute(sql, {"id":event_id})
    persons = result.fetchall()
    return persons
