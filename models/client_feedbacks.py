from init import db, ma
from marshmallow import fields
from datetime import date

from models.clients import ClientSchema



class Client_feedback(db.Model):
  __tablename__ = "client_feedback"

  id = db.Column(db.Integer, primary_key=True)  

  comments = db.Column(db.String(100), nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  date_submitted = db.Column(db.Date, nullable=False)
  client_id = db.Column(db.Integer, db.ForeignKey("clients.id", ondelete="CASCADE"))

  client = db.relationship("Client", back_populates="client_feedbacks")


class Client_feedbackSchema(ma.Schema):
  ordered=True
  client = fields.Nested("ClientSchema", only=["first_name", "last_name"])

  class Meta:
    fields = ("id", "comments", "rating", "date_submitted", "client_id", "client")

Client_feedback_Schema = Client_feedbackSchema()
Client_feedbacks_Schema = Client_feedbackSchema(many=True)