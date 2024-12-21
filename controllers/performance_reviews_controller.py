from flask import Blueprint
from init import ma, db
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
  
  
  