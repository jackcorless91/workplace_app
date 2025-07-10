import os
from flask import Flask
from dotenv import load_dotenv

from init import db, ma

from controllers.cli_controller import db_commands
from controllers.team_members_controller import team_members_bp
from controllers.rosters_controller import rosters_bp
from controllers.projects_controller import projects_bp
from controllers.performance_reviews_controller import performance_reviews_bp
from controllers.departments_controller import departments_bp
from controllers.clients_controller import clients_bp
from controllers.client_feedbacks_controller import client_feedbacks_bp


load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    app.json.sort_keys = False

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(team_members_bp)
    app.register_blueprint(rosters_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(performance_reviews_bp)
    app.register_blueprint(departments_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(client_feedbacks_bp)

    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app = create_app()
    app.run(host="0.0.0.0", port=port)