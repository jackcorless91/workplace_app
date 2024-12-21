from flask import Blueprint
from init import ma, db
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