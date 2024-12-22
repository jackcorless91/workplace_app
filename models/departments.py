from init import db, ma
from marshmallow import fields
from datetime import date


class Department(db.Model):
  __tablename__ = "departments"

  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String(100), nullable=False)
  speciality = db.Column(db.String(100), nullable=False)
  opening_time = db.Column(db.Time, nullable=False)
  closing_time = db.Column(db.Time, nullable=False)

  rosters = db.relationship("Roster", back_populates="department")



class DepartmentSchema(ma.Schema):
  ordered=True
  rosters = fields.List(fields.Nested("RosterSchema", exclude=["department"]))


  class Meta:
    fields = ("id", "name", "speciality", "opening_time", "closing_time", "rosters")

Department_Schema = DepartmentSchema()
Departments_Schema = DepartmentSchema(many=True)
