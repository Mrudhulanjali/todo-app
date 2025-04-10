
from flask import Flask
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
import os

from config import Config

mongo = PyMongo()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure MONGO_URI is set
    if not app.config.get("MONGO_URI"):
        # Fallback if not set in Config: set a default local URI
        app.config["MONGO_URI"] = "mongodb://localhost:27017/todo_db"

    mongo.init_app(app)
    csrf.init_app(app)

    # Optional test insert (remove or comment in production)
    # mongo.db.list.insert_one({"mrudhula": 123})

    from .auth import auth_bp
    from .routes import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app
