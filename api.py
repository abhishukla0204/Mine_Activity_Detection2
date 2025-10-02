"""
Flask API Backend for Mining Activity Monitoring Tool
Connects React frontend with Python analysis modules
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import uuid
import threading

# Import our mining modules
from src.utils.data_loader import DataLoader
from src.detection.mining_detector import MiningDetector
from src.detection.boundary_analyzer import BoundaryAnalyzer
from src.depth_volume.calculator import DepthVolumeCalculator
from src.visualization.map_2d import Map2DVisualizer
from src.visualization.map_3d import Map3DVisualizer
from src.report_generation.report_generator import ReportGenerator

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'tif', 'tiff', 'json', 'geojson', 'shp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Store analysis jobs
analysis_jobs = {}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def run_analysis(job_id, files, config):
    """Run the complete mining analysis pipeline"""
    try:
        # Update job status
        analysis_jobs[job_id]['status'] = 'processing'
        analysis_jobs[job_id]['progress'] = 10
        
        # Initialize components
        data_loader = DataLoader()
        
        # Step 1: Load data
        analysis_jobs[job_id]['current_step'] = 'Loading Data'
        satellite_data = data_loader.load_satellite_image(files['satellite'])
        dem_data = data_loader.load_dem(files['dem'])
        annotations = data_loader.load_coco_annotations(files['annotations'])
        analysis_jobs[job_id]['progress'] = 20
        
        # Step 2: Detect mining areas
        analysis_jobs[job_id]['current_step'] = 'Detecting Mining Areas'
        detector = MiningDetector()
        mining_polygons = detector.detect_from_annotations(annotations, satellite_data)
        analysis_jobs[job_id]['progress'] = 40
        
        # Step 3: Boundary analysis
        analysis_jobs[job_id]['current_step'] = 'Boundary Analysis'
        analyzer = BoundaryAnalyzer()
        if 'boundary' in files:
            boundary_data = data_loader.load_vector_file(files['boundary'])
            classification = analyzer.classify_mining_areas(mining_polygons, boundary_data)
        else:
            classification = {'legal': [], 'illegal': mining_polygons}
        analysis_jobs[job_id]['progress'] = 60
        
        # Step 4: Calculate depth and volume
        analysis_jobs[job_id]['current_step'] = 'Depth & Volume Calculation'
        calculator = DepthVolumeCalculator()
        results = []
        for idx, polygon in enumerate(mining_polygons):
            volume_info = calculator.process_mining_polygon(
                polygon, 
                dem_data, 
                method=config.get('volume_method', 'simpsons')
            )
            results.append({
                'id': idx + 1,
                'geometry': polygon.__geo_interface__,
                'area': polygon.area,
                'depth': volume_info.get('average_depth', 0),
                'volume': volume_info.get('volume', 0),
                'classification': 'legal' if polygon in classification.get('legal', []) else 'illegal'
            })
        analysis_jobs[job_id]['progress'] = 80
        
        # Step 5: Generate visualizations
        analysis_jobs[job_id]['current_step'] = 'Generating Visualizations'
        output_dir = os.path.join(RESULTS_FOLDER, job_id)
        os.makedirs(output_dir, exist_ok=True)
        
        visualizer_2d = Map2DVisualizer()
        map_file = visualizer_2d.create_classification_map(
            classification, 
            os.path.join(output_dir, 'map.html')
        )
        
        # Step 6: Generate report
        analysis_jobs[job_id]['current_step'] = 'Generating Report'
        report_gen = ReportGenerator()
        report_file = report_gen.generate_html_report(
            results,
            classification,
            os.path.join(output_dir, 'report.html')
        )
        analysis_jobs[job_id]['progress'] = 100
        
        # Update job with results
        analysis_jobs[job_id]['status'] = 'completed'
        analysis_jobs[job_id]['results'] = {
            'summary': {
                'total_sites': len(results),
                'total_area': sum(r['area'] for r in results),
                'total_volume': sum(r['volume'] for r in results),
                'legal_sites': len(classification.get('legal', [])),
                'illegal_sites': len(classification.get('illegal', [])),
            },
            'sites': results,
            'files': {
                'map': map_file,
                'report': report_file,
            }
        }
        
    except Exception as e:
        analysis_jobs[job_id]['status'] = 'failed'
        analysis_jobs[job_id]['error'] = str(e)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})


@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Upload satellite imagery, DEM, and annotations"""
    try:
        # Check if files are present
        required_files = ['satellite', 'dem', 'annotations']
        for file_type in required_files:
            if file_type not in request.files:
                return jsonify({'error': f'Missing {file_type} file'}), 400
        
        # Create unique job ID
        job_id = str(uuid.uuid4())
        job_dir = os.path.join(UPLOAD_FOLDER, job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        # Save uploaded files
        uploaded_files = {}
        for file_type in ['satellite', 'dem', 'annotations', 'boundary']:
            if file_type in request.files:
                file = request.files[file_type]
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(job_dir, filename)
                    file.save(filepath)
                    uploaded_files[file_type] = filepath
        
        # Create analysis job
        analysis_jobs[job_id] = {
            'id': job_id,
            'status': 'uploaded',
            'progress': 0,
            'current_step': 'Uploaded',
            'created_at': datetime.now().isoformat(),
            'files': uploaded_files
        }
        
        return jsonify({
            'job_id': job_id,
            'status': 'uploaded',
            'message': 'Files uploaded successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze/<job_id>', methods=['POST'])
def start_analysis(job_id):
    """Start analysis for uploaded files"""
    try:
        if job_id not in analysis_jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = analysis_jobs[job_id]
        if job['status'] != 'uploaded':
            return jsonify({'error': 'Job already processing or completed'}), 400
        
        # Get configuration
        config = request.json or {}
        
        # Start analysis in background thread
        thread = threading.Thread(
            target=run_analysis,
            args=(job_id, job['files'], config)
        )
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'status': 'processing',
            'message': 'Analysis started'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """Get analysis job status"""
    if job_id not in analysis_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = analysis_jobs[job_id]
    return jsonify({
        'job_id': job_id,
        'status': job['status'],
        'progress': job.get('progress', 0),
        'current_step': job.get('current_step', ''),
        'created_at': job['created_at']
    }), 200


@app.route('/api/results/<job_id>', methods=['GET'])
def get_results(job_id):
    """Get analysis results"""
    if job_id not in analysis_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = analysis_jobs[job_id]
    if job['status'] != 'completed':
        return jsonify({
            'error': 'Analysis not completed',
            'status': job['status']
        }), 400
    
    return jsonify(job['results']), 200


@app.route('/api/download/<job_id>/<file_type>', methods=['GET'])
def download_file(job_id, file_type):
    """Download generated files (report, map, etc.)"""
    if job_id not in analysis_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = analysis_jobs[job_id]
    if job['status'] != 'completed':
        return jsonify({'error': 'Analysis not completed'}), 400
    
    files = job['results'].get('files', {})
    if file_type not in files:
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(files[file_type], as_attachment=True)


@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """List all analysis jobs"""
    jobs_list = []
    for job_id, job in analysis_jobs.items():
        jobs_list.append({
            'job_id': job_id,
            'status': job['status'],
            'progress': job.get('progress', 0),
            'created_at': job['created_at']
        })
    
    return jsonify(jobs_list), 200


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get overall statistics from recent analyses"""
    # Mock statistics - in production, aggregate from database
    stats = {
        'total_analyses': len(analysis_jobs),
        'total_sites': 11,
        'total_area': 152.4,
        'legal_area': 98.6,
        'illegal_area': 53.8,
        'total_violations': 4,
        'total_volume': 4250000,
        'average_depth': 26.4
    }
    return jsonify(stats), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
