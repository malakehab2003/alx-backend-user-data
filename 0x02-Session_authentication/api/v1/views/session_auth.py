#!/usr/bin/env python3
""" new Flask view that handles all routes for the Session authentication """
from flask import request, jsonify
import os


from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def auth_session():
    """ login auth session """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(user) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(getattr(user[0], "id"))
    out = jsonify(user[0].to_json())
    out.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return out
