import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from database import db
from models import User

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def get_current_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return User.query.get(data['user_id'])
    except Exception:
        return None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'citizen')
    emergency_phone = data.get('emergency_phone', '')

    if not username or not email or not password:
        return jsonify({"error": "Username, email and password are required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User with this username or email already exists"}), 409

    user = User(
        username=username,
        email=email,
        role=role,
        emergency_phone=emergency_phone
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = generate_token(user.id)
    return jsonify({
        "message": "Registration successful",
        "user": user.to_dict(),
        "token": token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    identifier = data.get('identifier', '').strip() # username or email
    password = data.get('password', '').strip()

    if not identifier or not password:
        return jsonify({"error": "Username/email and password required"}), 400

    user = User.query.filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user.id)
    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "token": token
    })

@auth_bp.route('/me', methods=['GET'])
def get_me():
    user = get_current_user()
    if not user:
        # Return guest demo profile so app works gracefully in demo mode
        return jsonify({
            "is_guest": True,
            "user": {
                "id": 0,
                "username": "guest_explorer",
                "email": "guest@safestepspune.org",
                "role": "citizen",
                "emergency_phone": None
            }
        })
    return jsonify({
        "is_guest": False,
        "user": user.to_dict()
    })
