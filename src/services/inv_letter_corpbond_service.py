from flask import Blueprint, jsonify
from pymongo import MongoClient
from src.config import config
from src.config.db import get_connection_db
from src.repository.inv_letter_corpbond_repo import fetch_data
import logging
from decimal import Decimal
from datetime import date, datetime

def inv_letter_corpbond_get_all_data():
    try:
        conn = get_connection_db()
        datas = fetch_data(conn)
        return {
            "status": "success",
            "data": datas.get("data", [])
        }, 200
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500

def inv_letter_corpbond_sync_service():
    try:
        response, status_code = inv_letter_corpbond_get_all_data()
        
        if status_code != 200:
            logging.error(f"Failed to fetch data: Status {status_code}, Response: {response}")
            return jsonify({
                "status": "error",
                "message": f"Failed to fetch data: {response.get('message', 'Unknown error')}",
                "code": status_code
            }), status_code

        data = response.get("data", [])
        if not data:
            logging.warning("No data received from inv_letter_corpbond_get_all_data")
            return jsonify({
                "status": "warning",
                "message": "No data available to migrate",
                "code": 204
            }), 204

        mongo_client = MongoClient(config.MONGO_URI)
        mongo_db = mongo_client.get_default_database()
        mongo_collection = mongo_db[config.INV_LETTER_CORPBOND_COL]

        inserted_count = 0
        for row in data:
            if not isinstance(row, dict):
                logging.warning(f"Skipping invalid row data: {row}")
                continue

            document = {
                "acct_desc": row.get("acct_desc"),
                "addr1": row.get("addr1"),
                "addr2": row.get("addr2"),
                "addr3": row.get("addr3"),
                "ca_desc": row.get("ca_desc"),
                "client_code": row.get("client_code"),
                "code_base_cur": row.get("code_base_cur"),
                "eff_dt": decimal_default(row.get("eff_dt")),
                "invs_ktp_num": row.get("invs_ktp_num"),
                "invs_npw_num": row.get("invs_npw_num"),
                "invs_passport_num": row.get("invs_passport_num"),
                "mem_code": row.get("mem_code"),
                "mem_nm": row.get("mem_nm"),
                "next_day": decimal_default(row.get("next_day")),
                "rec_bal": decimal_default(row.get("rec_bal")),
                "rec_dt": decimal_default(row.get("rec_dt")),
                "sec_code": row.get("sec_code"),
                "sec_nm": row.get("sec_nm"),
                "trustee": row.get("trustee")
            }

            # Remove None values
            document = {k: v for k, v in document.items() if v is not None}

            result = mongo_collection.insert_one(document)
            if result.inserted_id:
                inserted_count += 1

        return jsonify({
            "status": "success",
            "message": f"Data migration completed. {inserted_count} records inserted.",
            "code": 200
        }), 200

    except Exception as e:
        logging.exception("Error during data migration")
        return jsonify({
            "status": "error",
            "message": f"Error during data migration: {str(e)}",
            "code": 500
        }), 500

    finally:
        if 'mongo_client' in locals():
            mongo_client.close()

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj) 
    elif isinstance(obj, date):
        return obj.isoformat()
    raise TypeError
