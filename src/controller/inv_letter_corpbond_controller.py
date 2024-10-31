from flask import Blueprint, jsonify
from src.services.inv_letter_corpbond_service import inv_letter_corpbond_get_all_data, inv_letter_corpbond_sync_service
import logging

inv_letter_corpbond_bp = Blueprint('inv_letter_corpbond', __name__)

@inv_letter_corpbond_bp.route('/data', methods=['GET'])
def inv_letter_corpbond_data():
    response_data, status_code = inv_letter_corpbond_get_all_data()
    return jsonify(response_data), status_code

@inv_letter_corpbond_bp.route('/sync', methods=['POST'])
def sync_inv_letter_corpbond():
    try:
        result, status_code = inv_letter_corpbond_sync_service()
        return result, status_code
    except Exception as e:
        logging.exception("Unexpected error in sync_inv_letter_corpbond")
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}",
            "code": 500
        }), 500 