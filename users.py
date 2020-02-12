from flask import Blueprint, request, jsonify, current_app
from flask_security.decorators import anonymous_user_required, login_required, auth_token_required
from flask_security.utils import hash_password, verify_password, login_user, logout_user
from models import User
from app import security

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/sign-up', methods=['POST'])
# @anonymous_user_required
def sign_up():
    post_data = request.get_json()
    email = post_data['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        pure_password = post_data['password']
        hashed_password = hash_password(pure_password)
        user = security.datastore.create_user(email=email, password=hashed_password)
        security.datastore.commit()
        return jsonify({
            'status': 'Success',
            'message': f'User is created. Please check your email for confirmation.'
        })
    else:
        return jsonify({'status': 'Failure', 'message': f"User with email '{email}' is already exists"}), 409


@users.route('/sign-in', methods=['POST'])
def sign_in():
    post_data = request.get_json()
    email = post_data['email']
    password = post_data['password']
    user = User.query.filter_by(email=email).first()
    if user and verify_password(password, user.password):
        token = user.get_auth_token()
        login_user(user)
        return jsonify({
            'status': 'Success',
            'payload': {
                'email': email,
                'token': token
            }
        })
    else:
        return jsonify({
            'status': 'Failure',
            'message': 'Your email or password is wrong'
        }), 403



@users.route('/sign-out', methods=['GET'])
@auth_token_required
def sign_out():
    logout_user()
    return jsonify({
        'status': 'Success',
        'message': 'You successfully sign out'
    })


@users.route('/<user_id>')
def get_user(user_id):
    pass
