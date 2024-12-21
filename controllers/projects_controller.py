from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
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
  


# POST (create new team member) /team_member
@projects_bp.route("/", methods=["POST"])
def create_project():
  try:
    body_data = request.get_json()
    new_project = Project(
      name=body_data.get("name"),
      description=body_data.get("description"),
      start_date=body_data.get("start_date"),
      due_date=body_data.get("due_date"),
    )
    db.session.add(new_project)
    db.session.commit()
    return Project_Schema.dump(new_project), 201
  except IntegrityError as err:
    print(err.orig.pgcode)
    if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
      return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
    
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
      return {"message": f"The field {err.orig.diag.constraint_name} is already in use"}, 409
  

# DELETE - /projects/id - DELETE
@projects_bp.route("/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
  stmt = db.select(Project).filter_by(id=project_id)
  project = db.session.scalar(stmt)
  if project:
    db.session.delete(project)
    db.session.commit()
    return {"message": f"Project {project} deleted successfully"}
  else:
    return {"message": f"Project with id {project} does not exist"}, 404
  

# update = /projects/id - PUT, PATCH
@projects_bp.route("/<int:project_id>", methods=["PUT", "PATCH"])
def update_project(project_id):
  try:
    stmt = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(stmt)
    body_data = request.get_json()
    if project:
      project.name = body_data.get("name") or project.name
      project.description = body_data.get("description") or project.description
      project.start_date = body_data.get("start_date") or project.start_date
      project.due_date = body_data.get("due_date") or project.due_date
      db.session.commit()
      return Project_Schema.dump(project)
    else:
      return {"message": f"Proje with id {project_id} does not exist"}, 404
  except IntegrityError:
    return {"message": f"Email address already in use"}, 409
  """
  update integreity error to check to multiple instead of just email
  """ 