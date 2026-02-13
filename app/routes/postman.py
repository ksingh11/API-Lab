from flask import Blueprint, jsonify, request
from app.utils.postman_generator import generate_postman_collection

bp = Blueprint('postman', __name__, url_prefix='/api/postman')

@bp.route('/collection', methods=['GET'])
def get_collection():
    """
    Download Postman Collection JSON.
    
    Query Parameters:
        base_url: Optional base URL (defaults to request host)
    
    Response:
        Postman Collection v2.1 JSON
    """
    # Get base URL from query params or use request host
    base_url = request.args.get('base_url')
    
    if not base_url:
        # Construct base URL from request
        base_url = f"{request.scheme}://{request.host}"
    
    collection = generate_postman_collection(base_url)
    
    response = jsonify(collection)
    response.headers['Content-Disposition'] = 'attachment; filename=API_Lab_Collection.json'
    
    return response, 200
