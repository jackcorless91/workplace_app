from init import ma, db
from datetime import date, time

class Performance_review(db.Model):
  __tablename__ = "performance_reviews"

  id = db.Column(db.Integer, primary_key=True)
  
  date = db.Column(db.Date, nullable=False)
  review_score = db.Column(db.Integer, nullable=False)
  comments = db.Column(db.String(500), nullable=True)

  """
  add team member foreign key
  """

class Performance_reviewSchema(ma.Schema):

  class Meta:
    fields = ("id", "date", "review_score", "comments")

Performance_reviewSchema = Performance_reviewSchema(many=True)