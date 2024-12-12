from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

from db import db
import routes




#ehkä, tässä alustetaan app ja sitten kutsuttaisin db:n uutta funktiota