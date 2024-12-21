from flask import Blueprint
from init import db, ma
from models.clients import Client, Clients_Schema

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")

@clients_bp.route("/")
def get_clients():
  stmt = db.select(Client)
  clients_list = db.session.scalars(stmt)
  data = Clients_Schema.dump(clients_list)
  return data