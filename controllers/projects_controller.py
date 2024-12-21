from flask import Blueprint
from init import db, ma
from models.projects import Project, Projects_Schema, Project_Schema

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")

@projects_bp.route("/")
def get_projects():
  stmt = db.select(Project)
  projects_list = db.session.scalars(stmt)
  data = Projects_Schema.dump(projects_list)
  return data

# GET (specfic project_id) /project/id

  

@projects_bp.route("/<int:project_id>")
def get_project(project_id):
  stmt = db.select(Project).filter_by(id=project_id)
  project = db.session.scalar(stmt)
  if project:
    data = Project_Schema.dump(project)
    return data
  else:
    return {"message": f"Team member with id {project_id} does not exist"}, 404