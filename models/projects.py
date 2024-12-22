from init import ma, db
from datetime import date, time

class Project(db.Model):
  __tablename_ = "projects"

  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String(100), nullable=False)
  description = db.Column(db.String(500), nullable=False)
  start_date = db.Column(db.Date, nullable=False)
  due_date = db.Column(db.Date)

  """
  add foreign key for team members and clients
  """

class ProjectSchema(ma.Schema):
  ordered=True

  class Meta:
    fields = ("id", "name", "description", "start_date", "due_date")

Project_Schema = ProjectSchema()
Projects_Schema = ProjectSchema(many=True)