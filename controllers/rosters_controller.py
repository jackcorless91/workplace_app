from flask import Blueprint
from init import db, ma
from models.rosters import Roster, Rosters_Schema, Roster_Schema

rosters_bp = Blueprint("rosters", __name__, url_prefix="/rosters")

@rosters_bp.route("/")
def get_rosters():
  stmt = db.select(Roster)
  rosters_list = db.session.scalars(stmt)
  data = Rosters_Schema.dump(rosters_list)
  return data


# GET (specific roster_id) /roster/id
@rosters_bp.route("/<int:roster_id>")
def get_roster(roster_id):
  stmt = db.select(Roster).filter_by(id=roster_id)
  roster = db.session.scalar(stmt)
  if roster:
    data = Roster_Schema.dump(roster)
    return data
  else:
    return {"message": f"Team member with id {roster_id} does not exist"}, 404
# POST (create new team member) /team_member
