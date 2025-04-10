import os

class Config:
    # Use environment variable if available, else fallback to local MongoDB URI
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/todo_db")

    # Secret key for session and CSRF protection
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")
