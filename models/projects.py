from init import ma, db
from datetime import date, time
from marshmallow import fields

from models.team_members import Team_memberSchema
from models.clients import ClientSchema



class Project(db.Model):
  __tablename_ = "projects"

  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String(100), nullable=False)
  description = db.Column(db.String(500), nullable=False)
  start_date = db.Column(db.Date, nullable=False)
  due_date = db.Column(db.Date)
  team_member_id = db.Column(db.Integer, db.ForeignKey("team_members.id", ondelete="CASCADE"))
  client_id = db.Column(db.Integer, db.ForeignKey("clients.id", ondelete="CASCADE"))

  team_member = db.relationship("Team_member", back_populates="projects")
  client = db.relationship("Client", back_populates="projects")



class ProjectSchema(ma.Schema):
  ordered=True
  team_member = fields.Nested("Team_memberSchema", only=["first_name", "last_name"])
  client = fields.Nested("ClientSchema", only=["first_name", "last_name"])

  class Meta:
    fields = ("id", "name", "description", "start_date", "due_date", "team_member_id", "team_member", "client_id", "client")

Project_Schema = ProjectSchema()
Projects_Schema = ProjectSchema(many=True)