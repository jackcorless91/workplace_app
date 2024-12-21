from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db, ma

from models.performance_reviews import Performance_review, Performance_reviews_Schema, Performance_review_Schema

performance_reviews_bp = Blueprint("performance_reviews", __name__, url_prefix="/performance_reviews")

@performance_reviews_bp.route("/")
def get_performance_reviews():
  stmt = db.select(Performance_review)
  performance_reviews_list = db.session.scalars(stmt)
  data = Performance_reviews_Schema.dump(performance_reviews_list)
  return data


# GET (specific performance review id) /performance_review/id
@performance_reviews_bp.route("/<int:performance_review_id>")
def get_performance_review(performance_review_id):
  stmt = db.select(Performance_review).filter_by(id=performance_review_id)
  performance_review = db.session.scalar(stmt)
  if performance_review:
    data = Performance_review_Schema.dump(performance_review)
    return data
  else:
    return {"message": f"Performance review with id {performance_review_id} does not exist"}, 404
  


# POST (create new performance review) /team_member
@performance_reviews_bp.route("/", methods=["POST"])
def create_performance_review():
  try:
    body_data = request.get_json()
    new_performance_review = Performance_review(
      date=body_data.get("date"),
      review_score=body_data.get("review_score"),
      comments=body_data.get("comments"),
    )
    db.session.add(new_performance_review)
    db.session.commit()
    return Performance_review_Schema.dump(new_performance_review), 201
  except IntegrityError as err:
    print(err.orig.pgcode)
    if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
      return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
    
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
      return {"message": f"The field {err.orig.diag.constraint_name} is already in use"}, 409
  
  
# DELETE - /performance_reviews/id - DELETE
@performance_reviews_bp.route("/<int:performance_review_id>", methods=["DELETE"])
def delete_performance_review(performance_review_id):
  stmt = db.select(Performance_review).filter_by(id=performance_review_id)
  performance_review = db.session.scalar(stmt)
  if performance_review:
    db.session.delete(performance_review)
    db.session.commit()
    return {"message": f"Project {performance_review} deleted successfully"}
  else:
    return {"message": f"Project with id {performance_review} does not exist"}, 404
  


# update = /rosters/id - PUT, PATCH
@performance_reviews_bp.route("/<int:performance_review_id>", methods=["PUT", "PATCH"])
def update_performance_review(performance_review_id):
  stmt = db.select(Performance_review).filter_by(id=performance_review_id)
  performance_review = db.session.scalar(stmt)
  body_data = request.get_json()
  if performance_review:
    performance_review.date = body_data.get("date") or performance_review.date
    performance_review.review_score = body_data.get("review_score") or performance_review.review_score
    performance_review.comments = body_data.get("comments") or performance_review.comments
    db.session.commit()
    return Performance_review_Schema.dump(performance_review)
  else:
    return {"message": f"Performance review with id {performance_review_id} does not exist"}, 404
  
"""
update integreity error to check to multiple instead of just email
"""