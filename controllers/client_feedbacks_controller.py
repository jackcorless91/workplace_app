from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db, ma

from models.client_feedbacks import Client_feedback, Client_feedbacks_Schema, Client_feedback_Schema


client_feedbacks_bp = Blueprint("client_feedbacks", __name__, url_prefix="/client_feedbacks")

@client_feedbacks_bp.route("/")
def get_client_feedbacks():
  stmt = db.select(Client_feedback)
  client_feedbacks_list = db.session.scalars(stmt)
  data = Client_feedbacks_Schema.dump(client_feedbacks_list)
  return data


# GET (specific client feedback)
@client_feedbacks_bp.route("/<int:client_feedback_id>")
def get_client_feedback(client_feedback_id):
  stmt = db.select(Client_feedback).filter_by(id=client_feedback_id)
  client_feedback = db.session.scalar(stmt)
  if client_feedback:
    data = Client_feedback_Schema.dump(client_feedback)
    return data
  else:
    return {"message": f"Client feedback with id {client_feedback_id} does not exist"}, 404
  


# POST (create new client feedback) /client_feedback
@client_feedbacks_bp.route("/", methods=["POST"])
def create_client_feedback():
  try:
    body_data = request.get_json()
    new_client_feedback  = Client_feedback(
      comments=body_data.get("comments"),
      rating=body_data.get("rating"),
      date_submitted=body_data.get("date_submitted"),
    )
    db.session.add(new_client_feedback)
    db.session.commit()
    return Client_feedback_Schema.dump(new_client_feedback), 201
  except IntegrityError as err:
    print(err.orig.pgcode)
    if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
      return {"message": f"The field {err.orig.diag.column_name} is required"}, 409
    
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
      return {"message": f"The field {err.orig.diag.constraint_name} is already in use"}, 409
    
  

# DELETE - /clients/id - DELETE
@client_feedbacks_bp.route("/<int:client_feedback_id>", methods=["DELETE"])
def delete_client_feedback(client_feedback_id):
  stmt = db.select(Client_feedback).filter_by(id=client_feedback_id)
  client_feedback = db.session.scalar(stmt)
  if client_feedback:
    db.session.delete(client_feedback)
    db.session.commit()
    return {"message": f"Client feedback {client_feedback} deleted successfully"}
  else:
    return {"message": f"Client feedback with id {client_feedback} does not exist"}, 404
  


@client_feedbacks_bp.route("/<int:client_feedback_id>", methods=["PUT", "PATCH"])
def update_client_feedback(client_feedback_id):
  stmt = db.select(Client_feedback).filter_by(id=client_feedback_id)
  client_feedback = db.session.scalar(stmt)
  body_data = request.get_json()
  if client_feedback:
    client_feedback.comments = body_data.get("comments") or client_feedback.comments
    client_feedback.rating = body_data.get("rating") or client_feedback.rating
    client_feedback.date_submitted = body_data.get("date_submitted") or client_feedback.date_submitted

    db.session.commit()
    return Client_feedback_Schema.dump(client_feedback)
  else:
    return {"message": f"Client feedback with id {client_feedback_id} does not exist"}, 404
  """
  update integreity error to check to multiple instead of just email
  """
