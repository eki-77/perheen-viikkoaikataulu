from db import db
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

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
        pw = getenv("ADMIN_PW", default="tsoha-admin")
        hash_value = generate_password_hash(pw)
        sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)")
        db.session.execute(sql, {"username":"admin", "password":hash_value, "admin":True})
        db.session.commit()
    else:
        print("löytyi admin")
