import os

from flask import Blueprint, request, jsonify
import traceback
from db import connect_to_db  # Import the database connection from db.py
from operations import process_csv_file, process_csv_file_role_dashboard

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/upload-dashboard-file', methods=['POST'])
def upload_dashboard_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file temporarily
    file_path = os.path.join("/tmp", file.filename)
    file.save(file_path)

    db = None
    try:
        db = connect_to_db()
        if db is None:
            raise ValueError("Failed to establish a database connection.")

        process_csv_file(file_path, db)

    except ValueError as ve:
        print(traceback.format_exc())
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        # Ensure database connection is closed
        if db:
            try:
                db.close()
            except Exception as e:
                print(f"Error closing database connection: {str(e)}")

    return jsonify({"message": "File processed successfully"}), 200

@api_blueprint.route('/upload-dashboard-role-file', methods=['POST'])
def upload_dashboard_role_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file temporarily
    file_path = os.path.join("/tmp", file.filename)
    file.save(file_path)

    db = None
    try:
        db = connect_to_db()
        if db is None:
            raise ValueError("Failed to establish a database connection.")

        process_csv_file_role_dashboard(file_path, db)

    except ValueError as ve:
        print(traceback.format_exc())
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        # Ensure database connection is closed
        if db:
            try:
                db.close()
            except Exception as e:
                print(f"Error closing database connection: {str(e)}")

    return jsonify({"message": "File processed successfully"}), 200