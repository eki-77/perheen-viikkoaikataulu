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
