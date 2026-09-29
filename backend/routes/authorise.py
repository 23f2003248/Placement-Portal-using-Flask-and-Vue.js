from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import request, Blueprint, jsonify
from models import db, User
from werkzeug.security import check_password_hash

auth_b = Blueprint('auth', __name__)

@auth_b.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(password)

    if not email or not password:
        return jsonify({"error":"all fields are required."}), 404
    
    user = User.query.filter_by(email = email).first()
    if not user:
        return jsonify({"error": "user not found."}), 404
    
    if user.is_active == False:
        return jsonify({"error": "user blacklisted."}), 401
    
    if check_password_hash(user.password, password):
        access_token = create_access_token(identity = email)
        return jsonify({
            "access_token": access_token,
            "role": user.role,
            "id": user.id
            }), 200
    
    return jsonify({"error":"password didnot match."}), 401