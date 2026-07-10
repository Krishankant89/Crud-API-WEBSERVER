from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Student   # <-- IMPORTANT
    from app.routes import api_bp

    with app.app_context():
        db.create_all()

    app.register_blueprint(api_bp)
    
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.errorhandler(404)
    def not_found(error):
        return{
            "error":"Resource not found"
                },404
    
    @app.errorhandler(500)
    def server_error(error):
        return{
            "error": "Internal Server Error"
                },500
    
    
    return app