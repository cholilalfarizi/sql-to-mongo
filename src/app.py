from flask import Flask, request, jsonify
from src.config import config
from src.controller.inv_letter_corpbond_controller import inv_letter_corpbond_bp
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
SWAGGER_URL="/swagger"
API_URL="/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)

CORS(app)


app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)

def authentication_api_key(api_key):
    try:
        if config.API_KEY == api_key:
            return True
        else:
            return False
    except Exception as e:
        return False
@app.route('/swagger.json')
def swagger():
    with open('src/swagger.json', 'r') as f:
        return jsonify(json.load(f))

@app.before_request
def before_request():
    if request.path.startswith('/swagger'):
        return
    api_key = request.headers.get('API-Key')
    if not api_key or not authentication_api_key(api_key):
        return jsonify({'error':'Unauthorized'}), 401
    
app.register_blueprint(inv_letter_corpbond_bp)