from init import db, ma
from datetime import date


class Roster(db.Model):
  __tablename__ = "rosters"

  id = db.Column(db.Integer, primary_key=True)

  start_time = db.Column(db.Time, nullable=False)
  end_time = db.Column(db.Time, nullable=False)
  shift_date = db.Column(db.Date, nullable=False)

  """
  add team member foreign key and department foreign key
  """

class RosterSchema(ma.Schema):
  ordered=True

  class Meta:
    fields = ("id", "start_time", "end_time", "shift_date")

Roster_Schema = RosterSchema()
Rosters_Schema = RosterSchema(many=True)