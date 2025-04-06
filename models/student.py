from utils.db import db

class Student(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    maths = db.Column(db.Integer, nullable=False)
    biology = db.Column(db.Integer, nullable=False)
    social =  db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Integer, nullable=False)