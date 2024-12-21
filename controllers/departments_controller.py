from flask import Blueprint
from init import db, ma
from models.departments import Department, Departments_Schema

departments_bp = Blueprint("departments", __name__, url_prefix="/departments")

@departments_bp.route("/")
def get_departments():
  stmt = db.select(Department)
  departments_list = db.session.scalars(stmt)
  data = Departments_Schema.dump(departments_list)
  return data