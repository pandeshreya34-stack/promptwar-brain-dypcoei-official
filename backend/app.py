import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import db
from seed import seed_database

from routes.auth_routes import auth_bp
from routes.places_routes import places_bp
from routes.routes_planner import routes_bp
from routes.itinerary_routes import itinerary_bp
from routes.safety_routes import safety_bp
from routes.civic_routes import civic_bp
from routes.assistant_routes import assistant_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend Vite development server & production origins
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    db.init_app(app)

    # Register Blueprints under /api
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(places_bp, url_prefix='/api')
    app.register_blueprint(routes_bp, url_prefix='/api')
    app.register_blueprint(itinerary_bp, url_prefix='/api')
    app.register_blueprint(safety_bp, url_prefix='/api')
    app.register_blueprint(civic_bp, url_prefix='/api')
    app.register_blueprint(assistant_bp, url_prefix='/api')

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "SEHER Pune Backend API — City Explorer & Safety Platform",
            "city": "Pune, Maharashtra, India",
            "demo_mode": app.config.get('DEMO_MODE', True),
            "version": "1.0.0"
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "An internal server error occurred"}), 500

    with app.app_context():
        db.create_all()
        seed_database()

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
