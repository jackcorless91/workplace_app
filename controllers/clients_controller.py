from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db, ma

from models.clients import Client, Clients_Schema, Client_Schema

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")

@clients_bp.route("/")
def get_clients():
  stmt = db.select(Client)
  clients_list = db.session.scalars(stmt)
  data = Clients_Schema.dump(clients_list)
  return data


# GET (specific client) /clients/id
@clients_bp.route("/<int:client_id>")
def get_client(client_id):
  stmt = db.select(Client).filter_by(id=client_id)
  client = db.session.scalar(stmt)
  if client:
    data = Client_Schema.dump(client)
    return data
  else:
    return {"message": f"Client with id {client_id} does not exist"}, 404
  


# POST (create new client) /team_member
@clients_bp.route("/", methods=["POST"])
def create_client():
  try:
    body_data = request.get_json()
    new_client = Client(
      first_name=body_data.get("first_name"),
      last_name=body_data.get("last_name"),
      email=body_data.get("email"),
      msisdn=body_data.get("msisdn"),
      company_name=body_data.get("company_name"),
      industry_type=body_data.get("industry_type"),
    )
    db.session.add(new_client)
    db.session.commit()
    return Client_Schema.dump(new_client), 201
  except IntegrityError as err:
    print(err.orig.pgcode)
    if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
      return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
    
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
      return {"message": f"The field {err.orig.diag.constraint_name} is already in use"}, 409

# DELETE - /clients/id - DELETE
@clients_bp.route("/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
  stmt = db.select(Client).filter_by(id=client_id)
  client = db.session.scalar(stmt)
  if client:
    db.session.delete(client)
    db.session.commit()
    return {"message": f"Client {client} deleted successfully"}
  else:
    return {"message": f"Client with id {client} does not exist"}, 404
  


# update = /clients/id - PUT, PATCH
@clients_bp.route("/<int:client_id>", methods=["PUT", "PATCH"])
def update_clients(client_id):

  stmt = db.select(Client).filter_by(id=client_id)
  client = db.session.scalar(stmt)
  body_data = request.get_json()
  if client:
    client.first_name = body_data.get("first_name") or client.first_name
    client.last_name = body_data.get("last_name") or client.last_name
    client.email = body_data.get("email") or client.email
    client.msisdn = body_data.get("msisdn") or client.msisdn
    client.company_name = body_data.get("company_name") or client.company_name
    client.industry_type = body_data.get("industry_type") or client.company_name
    
    db.session.commit()
    return Client_Schema.dump(client)
  else:
    return {"message": f"Roster with id {client_id} does not exist"}, 404
# except IntegrityError:
#   return {"message": f"Email address already in use"}, 409
"""
update integreity error to check to multiple instead of just email
"""
