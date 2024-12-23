from init import ma, db
from datetime import date, time
from marshmallow import fields

from models.team_members import Team_memberSchema
from models.departments import DepartmentSchema

class Roster(db.Model):
  __tablename__ = "rosters"

  id = db.Column(db.Integer, primary_key=True)

  start_time = db.Column(db.Time, nullable=False)
  end_time = db.Column(db.Time, nullable=False)
  shift_date = db.Column(db.Date, nullable=False)
  team_member_id = db.Column(db.Integer, db.ForeignKey("team_members.id", ondelete="CASCADE"))
  department_id = db.Column(db.Integer, db.ForeignKey("departments.id", ondelete="CASCADE"))

  team_member = db.relationship("Team_member", back_populates="rosters")
  department = db.relationship("Department", back_populates="rosters")



class RosterSchema(ma.Schema):
  ordered=True
  team_member = fields.Nested("Team_memberSchema", only=["first_name", "last_name"])
  department = fields.Nested("DepartmentSchema", only=["name", "opening_time", "closing_time"])
  class Meta:
    fields = ("id", "start_time", "end_time", "shift_date", "team_member_id", "team_member", "department_id", "department")

Roster_Schema = RosterSchema()
Rosters_Schema = RosterSchema(many=True)