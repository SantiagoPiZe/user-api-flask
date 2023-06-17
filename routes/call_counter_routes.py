from flask import Blueprint, jsonify, request
from app import db
from models import CallCounter

call_counter_routes = Blueprint('call_counter_routes', __name__)

@call_counter_routes.route('/call_counter', methods=['GET'])
def get_call_counter():
    
    call_counter = CallCounter.query.first()

    if not call_counter:
        return jsonify({'message': 'Call counter not found'}), 404

    response = {
        'calls': call_counter.count
    }


    return jsonify(response)