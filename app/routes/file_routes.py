from flask import Blueprint, request, jsonify
from app.services.file_service import read_xml_file
from http import HTTPStatus as HS

file_bp = Blueprint('file', __name__)


@file_bp.route('/api/file/read', methods=['POST'])
def read_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), HS.BAD_REQUEST

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), HS.BAD_REQUEST

    success = read_xml_file(file.stream, file.filename)
    return jsonify({'success': success}), HS.OK
