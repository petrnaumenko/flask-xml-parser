from flask import Blueprint, request, jsonify
from app.services.tag_service import get_tag_count, get_tag_attributes
from http import HTTPStatus as HS

tag_bp = Blueprint('tag', __name__)


@tag_bp.route('/api/tags/get-count', methods=['GET'])
def get_tag_count_route():
    file_name = request.args.get('file_name')
    tag_name = request.args.get('tag_name')
    
    if not file_name or not tag_name:
        return jsonify({'error': 'File name and tag name are required'}), HS.BAD_REQUEST
    
    try:
        count = get_tag_count(file_name, tag_name)
        return jsonify({'count': count}), HS.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HS.NOT_FOUND
    

@tag_bp.route('/api/tags/attributes/get', methods=['GET'])
def get_tag_attributes_route():
    file_name = request.args.get('file_name')
    tag_name = request.args.get('tag_name')
    
    if not file_name or not tag_name:
        return jsonify({'error': 'File name and tag name are required'}), HS.BAD_REQUEST
    
    try:
        attributes = get_tag_attributes(file_name, tag_name)
        return jsonify({'attributes': attributes}), HS.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HS.NOT_FOUND
