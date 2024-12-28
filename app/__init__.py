from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    from app.routes import main_bp
    from app.routes.diagram_routes import diagram_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(diagram_bp, url_prefix='/api/diagrams')

    return app 