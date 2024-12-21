from flask import Blueprint
from init import db, ma
from models.team_members import Team_member, Team_members_Schema

team_members_bp = Blueprint("team_members", __name__, url_prefix="/team_members")


@team_members_bp.route("/")
def get_team_members():
  stmt = db.select(Team_member)
  team_members_list = db.session.scalars(stmt)
  data = Team_members_Schema.dump(team_members_list)
  return data