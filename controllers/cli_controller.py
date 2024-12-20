from flask import Blueprint
from init import db,ma
from models.team_member import Team_member
from models.rosters import Roster
from models.projects import Project
from models.performance_reviews import Performance_review


db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
  db.create_all()
  print("Tables created")


@db_commands.cli.command("drop")
def drop_tables():
  db.drop_all()
  print("Tables dropped")


"""
need seed data for all tables **
"""

@db_commands.cli.command("seed")
def seed_tables():
    team_members = [
        Team_member()  
    ]
    rosters = [
        Roster()
    ],
    projects = [
       Project()
    ],
    performance_reviews = [
       Performance_review()
    ]
    db.session.add_all(team_members)
    db.session.add_all(rosters)
    db.session.add_all(projects)
    db.session.add_all(performance_reviews)
    db.session.commit()
    print("Tables seeded")