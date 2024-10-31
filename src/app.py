from flask import Flask, request, jsonify
from src.config import config
from src.controller.inv_letter_corpbond_controller import inv_letter_corpbond_bp
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config["MONGO_URI"] = config.MONGO_URI

app.register_blueprint(inv_letter_corpbond_bp)

# @app.route('/')
# def hello():
#     return "hello, world"

if __name__ == '__main__':
    app.run(debug=True)