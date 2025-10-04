from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from ..extensions import db


class Dummy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)