from flask import Blueprint, jsonify, request, send_file
from services.ml_service import recommend_crops, predict_yield, assess_pest_risk
from services.data_service import get_weather, get_market_prices, get_advisory, get_schemes
from services.report_service import build_report

report_bp = Blueprint('report', __name__)

@report_bp.route('/preview', methods=['POST'])
def preview():
    data = request.json
    district = data.get('district', 'Bardhaman')
    N   = float(data.get('N', 80))
    P   = float(data.get('P', 40))
    K   = float(data.get('K', 40))
    pH  = float(data.get('pH', 6.5))
    crop = data.get('crop', 'Rice (Aman)')
    season = data.get('season', 'Kharif')

    weather = get_weather(district)
    temp = weather['current']['temperature']
    hum  = weather['current']['humidity']
    rain = weather['current']['rainfall']

    recommendations = recommend_crops(N, P, K, pH, temp, rain, hum)
    yield_pred      = predict_yield(N, P, K, pH, temp, rain, hum, crop)
    pest_risks      = assess_pest_risk(temp, hum, crop)
    market_prices   = get_market_prices()
    advisory        = get_advisory(season)
    schemes         = get_schemes()

    return jsonify({
        'farmer': data,
        'weather': weather,
        'recommendations': recommendations,
        'yield_prediction': yield_pred,
        'pest_risks': pest_risks,
        'market_prices': market_prices,
        'advisory': advisory,
        'schemes': schemes,
    })

@report_bp.route('/generate', methods=['POST'])
def generate():
    data = request.json
    district = data.get('district', 'Bardhaman')
    N   = float(data.get('N', 80))
    P   = float(data.get('P', 40))
    K   = float(data.get('K', 40))
    pH  = float(data.get('pH', 6.5))
    crop = data.get('crop', 'Rice (Aman)')
    season = data.get('season', 'Kharif')

    weather = get_weather(district)
    temp = weather['current']['temperature']
    hum  = weather['current']['humidity']
    rain = weather['current']['rainfall']

    recommendations = recommend_crops(N, P, K, pH, temp, rain, hum)
    yield_pred      = predict_yield(N, P, K, pH, temp, rain, hum, crop)
    pest_risks      = assess_pest_risk(temp, hum, crop)
    market_prices   = get_market_prices()
    advisory        = get_advisory(season)
    schemes         = get_schemes()

    pdf_buffer = build_report(data, weather, recommendations, yield_pred,
                               pest_risks, market_prices, schemes, advisory)

    farmer_name = data.get('name', 'farmer').replace(' ', '_')
    filename = f"KVK_Report_{farmer_name}_{district}.pdf"

    return send_file(pdf_buffer, mimetype='application/pdf',
                     as_attachment=True, download_name=filename)
