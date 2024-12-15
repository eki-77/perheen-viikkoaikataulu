from sqlalchemy.sql import text
from flask import redirect, render_template, request, session
from db import db

def get_calendar(id):
    sql = text("SELECT * FROM calendars WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    cal = result.fetchone()
    if not cal:
        return False
    return cal

def update_cal(id, cal_name):
    sql = text("UPDATE calendars SET calendarname=:cal_name WHERE id=:id")
    result = db.session.execute(sql, {"cal_name":cal_name, "id":id})
    db.session.commit()
    return result

