from init import ma, db
from datetime import date, time
from marshmallow import fields

from models.team_members import Team_memberSchema

class Performance_review(db.Model):
  __tablename__ = "performance_reviews"

  id = db.Column(db.Integer, primary_key=True)
  
  date = db.Column(db.Date, nullable=False)
  review_score = db.Column(db.Integer, nullable=False)
  comments = db.Column(db.String(500), nullable=True)
  team_member_id = db.Column(db.Integer, db.ForeignKey("team_members.id"))

  team_member = db.relationship("Team_member", back_populates="performance_reviews")


class Performance_reviewSchema(ma.Schema):
  ordered=True
  team_member = fields.Nested("Team_memberSchema", only=["first_name", "last_name"])
  
  class Meta:
    fields = ("id", "date", "review_score", "comments", "team_member_id", "team_member")

Performance_review_Schema = Performance_reviewSchema()
Performance_reviews_Schema = Performance_reviewSchema(many=True)