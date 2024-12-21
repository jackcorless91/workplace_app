from flask import Blueprint
from init import db, ma
from models.rosters import Roster, Rosters_Schema

rosters_bp = Blueprint("rosters", __name__, url_prefix="/rosters")

@rosters_bp.route("/")
def get_rosters():
  stmt = db.select(Roster)
  rosters_list = db.session.scalars(stmt)
  data = Rosters_Schema.dump(rosters_list)
  return data