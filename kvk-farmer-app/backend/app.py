from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kvk-farmer-app-secret')

from routes.report import report_bp
from routes.chatbot import chatbot_bp
from routes.data import data_bp

app.register_blueprint(report_bp, url_prefix='/api/report')
app.register_blueprint(chatbot_bp, url_prefix='/api/chat')
app.register_blueprint(data_bp, url_prefix='/api/data')

@app.route('/api/health')
def health():
    return {'status': 'ok', 'message': 'KVK Farmer App Backend Running'}

if __name__ == '__main__':
    from services.ml_service import train_models
    print("Training ML models on startup...")
    train_models()
    print("Models ready.")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
