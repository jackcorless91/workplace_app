from flask import Blueprint
from init import db,ma
from datetime import date, time
from models.team_members import Team_member
from models.rosters import Roster
from models.projects import Project
from models.performance_reviews import Performance_review
from models.departments import Department
from models.clients import Client
from models.client_feedbacks import Client_feedback


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
      Team_member(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        msisdn=1234567890,
        start_date=date(2020, 1, 15),
        tenure=4,
        salary=55000
      )  
    ]

    db.session.add_all(team_members)
    db.session.commit()

    rosters = [
      Roster(
        start_time=time(9, 0),  
        end_time=time(17, 0),  
        shift_date=date(2024, 12, 21)  
      )
    ]

    db.session.add_all(rosters)
    db.session.commit()

    projects = [
      Project(
        name="Website Redesign",
        description="Redesign the company website to improve user experience and accessibility.",
        start_date=date(2024, 1, 15),
        due_date=date(2024, 3, 30)
      )
    ]
    
    db.session.add_all(projects)
    db.session.commit()

    performance_reviews = [
      Performance_review(
        date=date(2024, 1, 10),
        review_score=85,
        comments="Consistently meets expectations with exceptional performance in teamwork.",
        team_member_id=team_members[0].id
      )
    ]

    db.session.add_all(performance_reviews)
    db.session.commit()

    departments = [
      Department(
        name="Human Resources",
        speciality="Employee Relations",
        opening_time=time(9, 0),
        closing_time=time(17, 0)
      )
    ]

    db.session.add_all(departments)
    db.session.commit()

    clients = [
      Client(
        first_name="Alice",
        last_name="Johnson",
        email="alice.johnson@techhub.com",
        msisdn=1234567890,
        company_name="TechHub Solutions",
        industry_type="Technology"
      )
    ]

    db.session.add_all(clients)
    db.session.commit()

    client_feedbacks = [
        Client_feedback(
          comments="team member was good",
          rating=10,
          date_submitted=date(2024, 1, 10)
        )

    ]
    
    db.session.add_all(client_feedbacks)
    db.session.commit()

    print("Tables seeded")

