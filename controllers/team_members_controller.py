from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import datetime
from init import db, ma
from models.team_members import Team_member, Team_members_Schema, Team_member_Schema

team_members_bp = Blueprint("team_members", __name__, url_prefix="/team_members")

# GET (all team_members)
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
    try:
        body_data = request.get_json()

        new_team_member = Team_member(
            first_name=body_data.get("first_name"),
            last_name=body_data.get("last_name"),
            email=body_data.get("email"),
            msisdn=body_data.get("msisdn"),
            tenure=body_data.get("tenure"),
            salary=body_data.get("salary"),
        )

        db.session.add(new_team_member)
        db.session.commit()

        return Team_member_Schema.dump(new_team_member), 201

    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field {err.orig.diag.column_name} is required"}, 409

        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": f"The field {err.orig.diag.constraint_name} is already in use"}, 409

# DELETE - /team_members/id - DELETE
@team_members_bp.route("/<int:team_member_id>", methods=["DELETE"])
def delete_team_member(team_member_id):
    stmt = db.select(Team_member).filter_by(id=team_member_id)
    team_member = db.session.scalar(stmt)
    if team_member:
        db.session.delete(team_member)
        db.session.commit()
        return {"message": f"Team member {team_member} deleted successfully"}
    else:
        return {"message": f"Team member with id {team_member_id} does not exist"}, 404

# update = /students/id - PUT, PATCH
@team_members_bp.route("/<int:team_member_id>", methods=["PUT", "PATCH"])
def update_team_member(team_member_id):
    try:
        stmt = db.select(Team_member).filter_by(id=team_member_id)
        team_member = db.session.scalar(stmt)
        body_data = request.get_json()
        if team_member:
            team_member.first_name = body_data.get("first_name") or team_member.first_name
            team_member.last_name = body_data.get("last_name") or team_member.last_name
            team_member.email = body_data.get("email") or team_member.email
            team_member.msisdn = body_data.get("msisdn") or team_member.msisdn
            team_member.tenure = body_data.get("tenure") or team_member.tenure
            team_member.salary = body_data.get("salary") or team_member.salary
            db.session.commit()
            return Team_member_Schema.dump(team_member)
        else:
            return {"message": f"Team member with id {team_member_id} does not exist"}, 404
    except IntegrityError:
        return {"message": f"Email address already in use"}, 409
        """
  update integreity error to check to multiple instead of just email
       """
