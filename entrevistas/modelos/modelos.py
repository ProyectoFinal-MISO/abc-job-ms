from datetime import datetime
from enum import IntEnum
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

db = SQLAlchemy()

class Confirm(IntEnum):
    CONFIRMED = 1
    WAIT = 2
    REFUSED = 3

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 

class Meet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    place = db.Column(db.String(50))
    id_employee = db.Column(db.Integer)
    guests = db.relationship('Guest', backref='meet', lazy=True, cascade='all, delete-orphan')

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    name_user = db.Column(db.String(100))
    email_user = db.Column(db.String(100))
    type_user = db.Column(db.String(20))
    is_confirm = db.Column(db.String(20), default='WAIT')
    score = db.Column(db.Integer, default=-1)
    id_meet = db.Column(db.Integer, db.ForeignKey('meet.id'), nullable=False)

class GuestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Guest
        include_relationships = True
        load_instance = True

class MeetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Meet
        include_relationships = True
        load_instance = True
    guests = fields.Nested(GuestSchema, many=True)
