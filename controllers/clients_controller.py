from flask import Blueprint
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