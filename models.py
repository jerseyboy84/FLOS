import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

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


class Student(db.Model):
    __tablename__ = 'students'

    id = Column(db.Integer, primary_key=True)
    name = Column(String)
    studyLanguage = Column(String)
    nativeLanguage = Column(String)

    def __init__(self, name, studyLanguage, nativeLanguage):
        self.name = name
        self.studyLanguage = studyLanguage
        self.nativeLanguage = nativeLanguage

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
            'name': self.name,
            'studyLanguage': self.studyLanguage,
            'nativeLanguage': self.nativeLanguage
            }


class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = Column(db.Integer, primary_key=True)
    name = Column(String)
    teachLanguage = Column(String)
    fluentLanguage = Column(String)

    def __init__(self, name, teachLanguage, fluentLanguage):
        self.name = name
        self.teachLanguage = teachLanguage
        self.fluentLanguage = fluentLanguage

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
            'name': self.name,
            'teachLanguage': self.teachLanguage,
            'fluentLanguage': self.fluentLanguage
            }
