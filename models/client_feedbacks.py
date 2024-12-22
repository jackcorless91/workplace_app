from init import ma, db
from datetime import date, time

class Client_feedback(db.Model):
  __tablename__ = "client_feedback"

  id = db.Column(db.Integer, primary_key=True)  

  comments = db.Column(db.String(100), nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  date_submitted = db.Column(db.Date, nullable=False)

"""
project and client foreign keys to be added 
"""

class Client_feedbackSchema(ma.Schema):
  ordered=True
  class Meta:
    fields = ("id", "comments", "rating", "date_submitted")

Client_feedback_Schema = Client_feedbackSchema()
Client_feedbacks_Schema = Client_feedbackSchema(many=True)