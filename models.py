import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import backref
import psycopg2


ENV = 'prod'

if ENV == 'dev':
    database_name = "capstone"
    database_path = "postgres://{}:{}@{}/{}".format(
        'postgres', 'hade','localhost:5432', database_name)
else:
    database_name = "capstone"
    database_path = os.environ['DATABASE_URL']
    conn = psycopg2.connect(database_path, sslmode='require')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Drink

'''


class Drink(db.Model):
    __tablename__ = 'drink'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    combo = db.relationship('Combo', backref='drink', lazy=True)

    def __init__(self, title):
        self.title = title

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
        }



'''
Donut

'''


class Donut(db.Model):
    __tablename__ = 'donut'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    combo = db.relationship('Combo', backref='donut', lazy=True)

    def __init__(self, title):
        self.title = title

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
        }


'''
Combo
'''


class Combo(db.Model):
    __tablename__ = 'combo'
    # id = db.Column(db.Integer,  primary_key=True)
    id = db.Column(db.Integer, db.Sequence('seq_combo_id', start=1, increment=1),
               primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey(
        'drink.id'), nullable=False)
    donut_id = db.Column(db.Integer, db.ForeignKey(
        'donut.id'), nullable=False)

    def __init__(self, drink_id, donut_id):
        self.drink_id = drink_id
        self.donut_id = donut_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
