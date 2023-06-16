from flask import Blueprint, jsonify, request
from app import db
from models import User

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/user', methods=['GET'])
def search_users():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    first_name = request.args.get('first_name', default=None, type=str)
    last_name = request.args.get('last_name', default=None, type=str)
    email = request.args.get('email', default=None, type=str)

    query = User.query

    if first_name:
        query = query.filter(User.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(User.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    users = query.paginate(page=page, per_page=per_page)

    response = {
        'users': [user.serialize() for user in users.items],
        'total_users': users.total,
        'current_page': users.page,
        'per_page': users.per_page
    }

    return jsonify(response)

@user_routes.route('/user', methods=['POST'])
def create_user():
    data = request.json

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    if not first_name or not last_name or not email:
        return jsonify({'message': 'Missing required fields'}), 400

    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        return jsonify({'message': 'User with the same email already exists'}), 400
    
    user = User(first_name=first_name, last_name=last_name, email=email)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'user': user.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create user', 'error': str(e)}), 500
