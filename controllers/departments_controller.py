from flask import Blueprint
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