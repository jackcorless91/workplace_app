from flask import Blueprint, request
from init import db, ma
from models.team_members import Team_member, Team_members_Schema, Team_member_Schema

team_members_bp = Blueprint("team_members", __name__, url_prefix="/team_members")

# GET (all team_memebers)
@team_members_bp.route("/")
def get_team_members():
  stmt = db.select(Team_member)
  team_members_list = db.session.scalars(stmt)
  data = Team_members_Schema.dump(team_members_list)
  return data



# GET (specific team member) /team_member/id
@team_members_bp.route("/<int:team_member_id>")
def get_team_member(team_member_id):
  stmt = db.select(Team_member).filter_by(id=team_member_id)
  team_member = db.session.scalar(stmt)
  if team_member:
    data = Team_member_Schema.dump(team_member)
    return data
  else:
    return {"message": f"Team member with id {team_member_id} does not exist"}, 404


# POST (create new team member) /team_member
@team_members_bp.route("/", methods=["POST"])
def create_team_member():
  body_data = request.get_json()
  new_team_member  = Team_member(
    first_name=body_data.get("first_name"),
    last_name=body_data.get("last_name"),
    email=body_data.get("email"),
    msisdn=body_data.get("msisdn"),
    start_date=body_data.get("start_date"),
    tenure=body_data.get("tenure"),
    salary=body_data.get("salary"),
  )
  db.session.add(new_team_member)
  db.session.commit()
  return Team_member_Schema.dump(new_team_member), 201
# 