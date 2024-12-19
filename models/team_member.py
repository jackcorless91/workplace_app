from init import db, ma

from datetime import date

class Team_member(db.Model):
  __tablename__ = "team_members"

  id = db.Column(db.Integer, primary_key=True)

  first_name = db.Column(db.String(100), nullable=False)
  first_last = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)
  msisdn = db.Column(db.Integer(100), nullable=False, unique=True)
  # start_date = db.Column(db.Date, )
  tenure = db.Column(db.Integer(100), nullable=False)
  salary = db.column(db.Integer(100), nullable=False)

class Team_memberSchema(ma.Schema):
  class Meta:
    fields = ("id", "first_name", "last_name", "email", "msisdn", 'tenure', "salary")

Team_memberSchema = Team_memberSchema(many=True)
"""
change this later, unsure yet of complex and multiple relationship types
"""