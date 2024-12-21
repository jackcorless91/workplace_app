from flask import Blueprint
from init import ma, db
from models.performance_reviews import Performance_review, Performance_reviews_Schema

performance_reviews_bp = Blueprint("performance_reviews", __name__, url_prefix="/performance_reviews")

@performance_reviews_bp.route("/")
def get_performance_reviews():
  stmt = db.select(Performance_review)
  performance_reviews_list = db.session.scalars(stmt)
  data = Performance_reviews_Schema.dump(performance_reviews_list)
  return data