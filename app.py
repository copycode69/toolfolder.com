from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from rembg import remove
from PIL import Image

app = Flask(__name__)

# Set up directories for uploads and processed images
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Remove background using rembg
def remove_background(input_path, output_path):
    with open(input_path, 'rb') as input_file:
        input_image = input_file.read()
    output_image = remove(input_image)
    with open(output_path, 'wb') as output_file:
        output_file.write(output_image)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image (remove background)
        processed_image_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        remove_background(filepath, processed_image_path)

        return redirect(url_for('result', filename=filename))
    else:
        return "File type not allowed", 400

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
