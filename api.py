"""
Flask API Backend for Mining Activity Monitoring Tool
Serves pre-computed metrics from compute_real_metrics.py
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Path to computed metrics file
METRICS_FILE = 'frontend/public/computed_metrics.json'

def load_metrics():
    """Load computed metrics from JSON file"""
    try:
        if os.path.exists(METRICS_FILE):
            with open(METRICS_FILE, 'r') as f:
                return json.load(f)
        else:
            return None
    except Exception as e:
        print(f"Error loading metrics: {e}")
        return None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    })


@app.route('/api/sites', methods=['GET'])
def get_sites():
    """Get all mining sites"""
    data = load_metrics()
    if data is None:
        return jsonify({'error': 'Metrics not found'}), 404
    
    return jsonify({
        'sites': data.get('mines', []),
        'total': len(data.get('mines', []))
    })


@app.route('/api/sites/<int:site_id>', methods=['GET'])
def get_site(site_id):
    """Get specific mining site by ID"""
    data = load_metrics()
    if data is None:
        return jsonify({'error': 'Metrics not found'}), 404
    
    mines = data.get('mines', [])
    site = next((m for m in mines if m['id'] == site_id), None)
    
    if site is None:
        return jsonify({'error': 'Site not found'}), 404
    
    return jsonify(site)


@app.route('/api/sites/legal', methods=['GET'])
def get_legal_sites():
    """Get all legal mining sites"""
    data = load_metrics()
    if data is None:
        return jsonify({'error': 'Metrics not found'}), 404
    
    legal_sites = [m for m in data.get('mines', []) if m['type'] == 'legal']
    
    return jsonify({
        'sites': legal_sites,
        'total': len(legal_sites)
    })


@app.route('/api/sites/illegal', methods=['GET'])
def get_illegal_sites():
    """Get all illegal mining sites"""
    data = load_metrics()
    if data is None:
        return jsonify({'error': 'Metrics not found'}), 404
    
    illegal_sites = [m for m in data.get('mines', []) if m['type'] == 'illegal']
    
    return jsonify({
        'sites': illegal_sites,
        'total': len(illegal_sites)
    })


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get aggregate mining statistics"""
    data = load_metrics()
    if data is None:
        return jsonify({'error': 'Metrics not found'}), 404
    
    metadata = data.get('metadata', {})
    mines = data.get('mines', [])
    
    # Calculate statistics
    legal_sites = [m for m in mines if m['type'] == 'legal']
    illegal_sites = [m for m in mines if m['type'] == 'illegal']
    
    legal_area = sum(m['area'] for m in legal_sites)
    illegal_area = sum(m['area'] for m in illegal_sites)
    
    depths = [m['depth'] for m in mines if m['depth'] > 0]
    avg_depth = sum(depths) / len(depths) if depths else 0
    
    return jsonify({
        'total_sites': metadata.get('total_mines', len(mines)),
        'legal_sites': metadata.get('legal_mines', len(legal_sites)),
        'illegal_sites': metadata.get('illegal_mines', len(illegal_sites)),
        'total_area': metadata.get('total_area_ha', legal_area + illegal_area),
        'legal_area': metadata.get('legal_area_ha', legal_area),
        'illegal_area': metadata.get('illegal_area_ha', illegal_area),
        'total_volume': metadata.get('total_volume_m3', sum(m['volume'] for m in mines)),
        'average_depth': round(avg_depth, 2)
    })


@app.route('/api/sites/search', methods=['GET'])
def search_sites():
    """Search sites with filters"""
    from flask import request
    
    data = load_metrics()
    if data is None:
        return jsonify({'error': 'Metrics not found'}), 404
    
    mines = data.get('mines', [])
    
    # Get query parameters
    operator = request.args.get('operator', '').lower()
    min_area = request.args.get('minArea', type=float)
    max_area = request.args.get('maxArea', type=float)
    min_depth = request.args.get('minDepth', type=float)
    max_depth = request.args.get('maxDepth', type=float)
    site_type = request.args.get('type', '').lower()
    
    # Filter mines
    filtered = mines
    
    if operator:
        filtered = [m for m in filtered if operator in m.get('operator', '').lower()]
    
    if min_area is not None:
        filtered = [m for m in filtered if m['area'] >= min_area]
    
    if max_area is not None:
        filtered = [m for m in filtered if m['area'] <= max_area]
    
    if min_depth is not None:
        filtered = [m for m in filtered if m['depth'] >= min_depth]
    
    if max_depth is not None:
        filtered = [m for m in filtered if m['depth'] <= max_depth]
    
    if site_type:
        filtered = [m for m in filtered if m['type'] == site_type]
    
    return jsonify({
        'sites': filtered,
        'total': len(filtered),
        'filters_applied': {
            'operator': operator or None,
            'min_area': min_area,
            'max_area': max_area,
            'min_depth': min_depth,
            'max_depth': max_depth,
            'type': site_type or None
        }
    })


@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate custom report (placeholder)"""
    from flask import request
    
    data = load_metrics()
    if data is None:
        return jsonify({'error': 'Metrics not found'}), 404
    
    # Get requested site IDs
    req_data = request.json or {}
    site_ids = req_data.get('site_ids', [])
    format_type = req_data.get('format', 'json')
    
    mines = data.get('mines', [])
    
    if site_ids:
        selected_sites = [m for m in mines if m['id'] in site_ids]
    else:
        selected_sites = mines
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'format': format_type,
        'total_sites': len(selected_sites),
        'sites': selected_sites,
        'summary': {
            'total_area': sum(m['area'] for m in selected_sites),
            'total_volume': sum(m['volume'] for m in selected_sites),
            'legal_count': len([m for m in selected_sites if m['type'] == 'legal']),
            'illegal_count': len([m for m in selected_sites if m['type'] == 'illegal'])
        }
    }
    
    return jsonify(report)


if __name__ == '__main__':
    print("=" * 60)
    print("Mining Activity Monitoring Tool - API Server")
    print("=" * 60)
    print(f"\nLoading metrics from: {METRICS_FILE}")
    
    data = load_metrics()
    if data:
        print(f"✓ Loaded {len(data.get('mines', []))} mining sites")
        print(f"✓ Total area: {data.get('metadata', {}).get('total_area_ha', 0):.2f} ha")
        print(f"✓ Total volume: {data.get('metadata', {}).get('total_volume_m3', 0):,.0f} m³")
    else:
        print("✗ Warning: Could not load metrics file")
        print("  Run: python compute_real_metrics.py")
    
    print("\n" + "=" * 60)
    print("Starting API server on http://localhost:5000")
    print("=" * 60)
    print("\nEndpoints:")
    print("  GET  /api/health")
    print("  GET  /api/sites")
    print("  GET  /api/sites/<id>")
    print("  GET  /api/sites/legal")
    print("  GET  /api/sites/illegal")
    print("  GET  /api/stats")
    print("  GET  /api/sites/search")
    print("  POST /api/generate-report")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
