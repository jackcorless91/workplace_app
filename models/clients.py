from init import db, ma
from datetime import date, time

class Client(db.Model):
  __tablename__ = "clients"

  id = db.Column(db.Integer, primary_key=True)

  first_name = db.Column(db.String(100), nullable=False)
  last_name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)
  msisdn = db.Column(db.Integer, nullable=False, unique=True)
  company_name = db.Column(db.String(100), nullable=False)
  industry_type = db.Column(db.String(100), nullable=False)

  """
  no foreign key
  """

class ClientSchema(ma.Schema):
  ordered=True
  class Meta:
    fields = ("id", "first_name", "last_name", "email", "msisdn", "company_name", "industry_name")

Client_Schema = ClientSchema()
Clients_Schema = ClientSchema(many=True)