from flask import Blueprint, jsonify, request
from app import db
from models import Organization, CallCounter

organization_routes = Blueprint('organization_routes', __name__)

@organization_routes.before_app_request
def create_counter():
    counter = CallCounter.query.first()
    if not counter:
        counter = CallCounter(count=0)
        db.session.add(counter)
        db.session.commit()

@organization_routes.before_request
def increment_counter():
    counter = CallCounter.query.first()
    counter.count += 1
    db.session.commit()

@organization_routes.route('/organization', methods=['GET'])
def search_organizations():

    organizations = Organization.query.all()

    response = {
        'organizations': [organization.serialize() for organization in organizations]
    }

    return jsonify(response)

@organization_routes.route('/organization', methods=['POST'])
def create_organization():

    data = request.json

    name = data.get('name')

    if not name:
        return jsonify({'message': 'Name is required'}), 400
    
    organization = Organization(name=name)

    try:
        db.session.add(organization)
        db.session.commit()
        return jsonify({'message': 'Organization created successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong'}), 400
