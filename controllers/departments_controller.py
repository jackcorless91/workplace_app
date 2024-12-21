from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db, ma

from models.departments import Department, Departments_Schema, Department_Schema

departments_bp = Blueprint("departments", __name__, url_prefix="/departments")

@departments_bp.route("/")
def get_departments():
  stmt = db.select(Department)
  departments_list = db.session.scalars(stmt)
  data = Departments_Schema.dump(departments_list)
  return data


# GET (specific department id) /department/id
@departments_bp.route("/<int:department_id>")
def get_department(department_id):
  stmt = db.select(Department).filter_by(id=department_id)
  department = db.session.scalar(stmt)
  if department:
    data = Department_Schema.dump(department)
    return data
  else:
    return{"message": f"Department with id {department_id} does not exist"}, 404
  


# POST (create new team member) /team_member
@departments_bp.route("/", methods=["POST"])
def create_department():
  try:
    body_data = request.get_json()
    new_department = Department(
      name=body_data.get("name"),
      speciality=body_data.get("speciality"),
      opening_time=body_data.get("opening_time"),
      closing_time=body_data.get("closing_time"),
    )
    db.session.add(new_department)
    db.session.commit()
    return Department_Schema.dump(new_department), 201
  except IntegrityError as err:
    print(err.orig.pgcode)
    if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
      return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
    
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
      return {"message": f"The field {err.orig.diag.constraint_name} is already in use"}, 409
  

# DELETE - /departments/id - DELETE
@departments_bp.route("/<int:department_id>", methods=["DELETE"])
def delete_department(department_id):
  stmt = db.select(Department).filter_by(id=department_id)
  department = db.session.scalar(stmt)
  if department:
    db.session.delete(department)
    db.session.commit()
    return {"message": f"Project {department} deleted successfully"}
  else:
    return {"message": f"Project with id {department} does not exist"}, 404
  


# update = /department/id - PUT, PATCH
@departments_bp.route("/<int:department_id>", methods=["PUT", "PATCH"])
def update_department(department_id):

  stmt = db.select(Department).filter_by(id=department_id)
  department = db.session.scalar(stmt)
  body_data = request.get_json()
  if department:
    department.name = body_data.get("name") or department.name
    department.speciality = body_data.get("speciality") or department.speciality
    department.opening_time = body_data.get("opening_time") or department.opening_time
    department.closing_time = body_data.get("closing_time") or department.opening_time

    db.session.commit()
    return Department_Schema.dump(department)
  else:
    return {"message": f"Department with id {department_id} does not exist"}, 404
"""
update integreity error to check to multiple instead of just email
"""