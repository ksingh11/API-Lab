from flask import Blueprint, jsonify
from app.utils.scenarios import get_all_scenarios, get_scenario

bp = Blueprint('scenarios', __name__, url_prefix='/api/scenarios')

@bp.route('', methods=['GET'])
def list_scenarios():
    """
    Get all available learning scenarios.
    
    Response:
        {
            "data": [...],
            "count": 4
        }
    """
    scenarios = get_all_scenarios()
    
    # Return summary (without full steps for performance)
    summaries = [
        {
            'id': s['id'],
            'name': s['name'],
            'description': s['description'],
            'difficulty': s['difficulty'],
            'duration': s['duration'],
            'step_count': len(s['steps'])
        }
        for s in scenarios
    ]
    
    return jsonify({
        'data': summaries,
        'count': len(summaries)
    }), 200

@bp.route('/<scenario_id>', methods=['GET'])
def get_scenario_details(scenario_id):
    """
    Get full details of a specific scenario including all steps.
    
    Response:
        {
            "data": {...}
        }
    """
    scenario = get_scenario(scenario_id)
    
    if not scenario:
        return jsonify({
            'error': 'Scenario not found',
            'code': 'SCENARIO_NOT_FOUND'
        }), 404
    
    return jsonify({
        'data': scenario
    }), 200
