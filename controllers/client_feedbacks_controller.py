from flask import Blueprint
from init import ma, db
from models.client_feedbacks import Client_feedback, Client_feedbacks_Schema


client_feedbacks_bp = Blueprint("client_feedbacks", __name__, url_prefix="/client_feedbacks")

@client_feedbacks_bp.route("/")
def get_client_feedbacks():
  stmt = db.select(Client_feedback)
  client_feedbacks_list = db.session.scalars(stmt)
  data = Client_feedbacks_Schema.dump(client_feedbacks_list)
  return data