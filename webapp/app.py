
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.analysis_service import run_full_analysis

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'replays')
ANALYSIS_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'replays-analysis')
ALLOWED_EXTENSIONS = {'sc2replay'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'replay_file' not in request.files:
        return redirect(request.url)
    file = request.files['replay_file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        replay_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(replay_path)

        analyze_option = request.form.get('analyze_option') == 'true'
        visualize_option = request.form.get('visualize_option') == 'true'

        # Run the analysis using the core service
        results = run_full_analysis(replay_path, analyze_option, visualize_option)

        return render_template('results.html', 
                               alerts=results['alerts'], 
                               replay_name=results['replay_name'],
                               players=results['players'],
                               teams=results['teams'],
                               player_stats=results['player_stats'],
                               build_orders=results['build_orders'],
                               charts=results['charts'])

    return redirect(url_for('index'))

@app.route('/replays-analysis/<path:filename>')
def serve_analysis_file(filename):
    return send_from_directory(ANALYSIS_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

