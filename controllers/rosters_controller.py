from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
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
@rosters_bp.route("/", methods=["POST"])
def create_roster():
  try:
    body_data = request.get_json()
    new_roster = Roster(
      start_time=body_data.get("start_time"),
      end_time=body_data.get("end_time"),
      shift_date=body_data.get("shift_date"),
    )
    db.session.add(new_roster)
    db.session.commit()
    return Roster_Schema.dump(new_roster), 201
  except IntegrityError as err:
    print(err.orig.pgcode)
    if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
      return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
    
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
      return {"message": f"The field {err.orig.diag.constraint_name} is already in use"}, 409


# DELETE - /rosters/id - DELETE
@rosters_bp.route("/<int:roster_id>", methods=["DELETE"])
def delete_roster(roster_id):
  stmt = db.select(Roster).filter_by(id=roster_id)
  roster = db.session.scalar(stmt)
  if roster:
    db.session.delete(roster)
    db.session.commit()
    return {"message": f"Roster {roster} deleted successfully"}
  else:
    return {"message": f"Roster with id {roster} does not exist"}, 404


# update = /rosters/id - PUT, PATCH
@rosters_bp.route("/<int:roster_id>", methods=["PUT", "PATCH"])
def update_roster(roster_id):

  stmt = db.select(Roster).filter_by(id=roster_id)
  roster = db.session.scalar(stmt)
  body_data = request.get_json()
  if roster:
    roster.start_time = body_data.get("start_time") or roster.start_time
    roster.end_time = body_data.get("end_time") or roster.start_time
    roster.shift_date = body_data.get("shift_date") or roster.start_time
    db.session.commit()
    return Roster_Schema.dump(roster)
  else:
    return {"message": f"Roster with id {roster_id} does not exist"}, 404
# except IntegrityError:
#   return {"message": f"Email address already in use"}, 409
"""
update integreity error to check to multiple instead of just email
"""


    