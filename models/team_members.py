from init import db, ma

from datetime import date

class Team_member(db.Model):
  __tablename__ = "team_members"

  id = db.Column(db.Integer, primary_key=True)

  first_name = db.Column(db.String(100), nullable=False)
  last_name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)
  msisdn = db.Column(db.Integer, nullable=False, unique=True)
  start_date = db.Column(db.Date, nullable=False)
  tenure = db.Column(db.Integer, nullable=False)
  salary = db.Column(db.Integer, nullable=False)

  """
  no foreign keys to add
  """

class Team_memberSchema(ma.Schema):
  class Meta:
    fields = ("id", "first_name", "last_name", "email", "msisdn", 'tenure', "salary")

Team_member_Schema = Team_memberSchema()
Team_members_Schema = Team_memberSchema(many=True)
