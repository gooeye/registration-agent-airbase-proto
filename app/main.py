import os
from flask import Flask, request, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from app.utils import process_file
import time

app = Flask(__name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_files'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure upload and processed folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_filepath)

        file_extension = filename.rsplit('.', 1)[1].lower()
        processed_filename = f"processed_{filename}"
        output_filepath = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)

        if process_file(input_filepath, output_filepath, file_extension):
            time.sleep(5) # Simulate processing time
            with open(output_filepath, 'rb') as f:
                file_data = f.read()
            return file_data, 200, {'Content-Type': 'application/octet-stream', 'Content-Disposition': f'attachment; filename={processed_filename}'}
        else:
            return jsonify({'error': 'File processing failed'}), 500
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')