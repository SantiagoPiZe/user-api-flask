from flask import Blueprint, jsonify, request
from app import db
from models import User, Organization, CallCounter

user_routes = Blueprint('user_routes', __name__)

@user_routes.before_app_request
def create_counter():
    counter = CallCounter.query.first()
    if not counter:
        counter = CallCounter(count=0)
        db.session.add(counter)
        db.session.commit()

@user_routes.before_request
def increment_counter():
    counter = CallCounter.query.first()
    counter.count += 1
    db.session.commit()

@user_routes.route('/user', methods=['GET'])
def search_users():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    first_name = request.args.get('first_name', default=None, type=str)
    last_name = request.args.get('last_name', default=None, type=str)
    email = request.args.get('email', default=None, type=str)
    organization_id = request.args.get('organization_id', default=None, type=int)

    query = User.query

    if first_name:
        query = query.filter(User.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(User.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if organization_id:
        query = query.filter(User.organizations.any(id=organization_id))

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

@user_routes.route('/user/assign_organization', methods=['POST'])
def assign_organization():
    
    data = request.json

    user_id = data.get('user_id')
    organization_id = data.get('organization_id')

    if not user_id or not organization_id:
        return jsonify({'message': 'Missing user_id or organization_id'}), 400

    user = User.query.get(user_id)
    organization = Organization.query.get(organization_id)

    if not user or not organization:
        return jsonify({'message': 'User or Organization not found'}), 404
    
    if organization in user.organizations:
        return jsonify({'message': 'User is already assigned to this organization'}), 400

    user.organizations.append(organization)
    db.session.commit()

    return jsonify({'message': 'User assigned to organization successfully'})
