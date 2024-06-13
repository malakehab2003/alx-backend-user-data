#!/usr/bin/env python3
""" create flask app """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def index() -> str:
    """ create / route """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ create /users route """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ create login page """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
    except Exception:
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    display = jsonify({"email": email, "message": "logged in"})
    display.set_cookie("session_id", session_id)
    return display


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ destroy session """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        redirect("/")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
