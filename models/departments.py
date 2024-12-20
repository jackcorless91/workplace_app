from init import ma, db
from datetime import date, time

class Department(db.Model):
  __tablename__ = "departments"

  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String(100), nullable=False)
  speciality = db.Column(db.String(100), nullable=False)
  opening_time = db.Column(db.Time, nullable=False)
  closing_time = db.Column(db.Time, nullable=False)

  """
  no foreign key
  """

class DepartmentSchema(ma.Schema):

  class Meta:
    fields = ("id", "name", "speciality", "opening_time", "closing_time")

Department_Schema = DepartmentSchema()
Departments_Schema = DepartmentSchema(many=True)
