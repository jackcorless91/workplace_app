from flask import Blueprint
from init import db, ma
from models.projects import Project, Projects_Schema

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")

@projects_bp.route("/")
def get_projects():
  stmt = db.select(Project)
  projects_list = db.session.scalars(stmt)
  data = Projects_Schema.dump(projects_list)
  return data