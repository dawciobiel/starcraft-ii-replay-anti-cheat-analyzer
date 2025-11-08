import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
import configparser
import sqlite3
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser.parser_v1_0 import parse_replay
from analyzer.analyzer import analyze_replay

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'replays')
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

        # --- Analysis Logic ---
        base_analysis_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', "replays-analysis")
        replay_base_name = os.path.splitext(filename)[0]
        
        config = configparser.ConfigParser(interpolation=None)
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config', 'config.ini'))
        timestamp_format = config.get('Analyzer', 'TimestampFormat', fallback='%Y-%m-%d_%H-%M-%S')
        
        timestamp = datetime.datetime.now().strftime(timestamp_format)
        
        current_analysis_dir = os.path.join(base_analysis_dir, replay_base_name, timestamp)
        os.makedirs(current_analysis_dir, exist_ok=True)
        
        parser_db_name = f"{replay_base_name}.parser-v1.0.db"
        db_path = os.path.join(current_analysis_dir, parser_db_name)
        
        parse_replay(replay_path, db_path)
        analyze_replay(db_path, current_analysis_dir)
        
        # --- Read results ---
        alerts = []
        alerts_file_path = os.path.join(current_analysis_dir, 'alerts.json')
        if os.path.exists(alerts_file_path):
            with open(alerts_file_path, 'r') as f:
                alerts = f.read()

        return render_template('results.html', alerts=alerts, replay_name=filename)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
