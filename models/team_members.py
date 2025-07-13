from init import db, ma
from marshmallow import fields
from datetime import date


class Team_member(db.Model):
  __tablename__ = "team_members"

  id = db.Column(db.Integer, primary_key=True)

  first_name = db.Column(db.String(100), nullable=False)
  last_name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)
  msisdn = db.Column(db.Integer, nullable=False, unique=True)
  tenure = db.Column(db.Integer, nullable=False)
  salary = db.Column(db.Integer, nullable=False)

  performance_reviews = db.relationship("Performance_review", back_populates="team_member")
  rosters = db.relationship("Roster", back_populates="team_member")
  projects = db.relationship("Project", back_populates="team_member")


class Team_memberSchema(ma.Schema):
  ordered=True
  performance_reviews = fields.List(fields.Nested("Performance_reviewSchema", exclude=["team_member"]))
  rosters = fields.List(fields.Nested("RosterSchema", exclude=["team_member"]))
  projects = fields.List(fields.Nested("ProjectSchema", exclude=["team_member"]))

  class Meta:
    fields = ("id", "first_name", "last_name", "email", "msisdn", 'tenure', "salary", "performance_reviews", "rosters", "projects")

Team_member_Schema = Team_memberSchema()
Team_members_Schema = Team_memberSchema(many=True)
