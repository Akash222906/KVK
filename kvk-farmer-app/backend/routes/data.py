from flask import Blueprint, jsonify, request
from services.data_service import get_weather, get_market_prices, get_advisory, get_schemes, get_districts

data_bp = Blueprint('data', __name__)

@data_bp.route('/weather/<district>', methods=['GET'])
def weather(district):
    return jsonify(get_weather(district))

@data_bp.route('/market', methods=['GET'])
def market():
    return jsonify(get_market_prices())

@data_bp.route('/advisory', methods=['GET'])
def advisory():
    season = request.args.get('season', 'Kharif')
    return jsonify(get_advisory(season))

@data_bp.route('/schemes', methods=['GET'])
def schemes():
    return jsonify(get_schemes())

@data_bp.route('/districts', methods=['GET'])
def districts():
    return jsonify(get_districts())
