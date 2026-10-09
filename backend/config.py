import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'safesteps-pune-hackathon-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///safesteps_pune.db')
    # If postgresql:// is provided in modern Render / Heroku without +psycopg, handle postgres://
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEMO_MODE = os.environ.get('DEMO_MODE', 'true').lower() in ['true', '1', 'yes']
    PUNE_CENTER = {
        "lat": 18.5204,
        "lng": 73.8567
    }
