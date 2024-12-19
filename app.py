from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from tools.rembg_tool import remove_background  # Import the custom tool

app = Flask(__name__)

# Configuration for file upload and processed image
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create necessary directories if not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to render the upload form and process the image
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the file is valid and its extension is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            # Process the image
            processed_filename = 'processed_' + filename
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            
            # Call the remove_background function (Ensure you have this tool)
            try:
                remove_background(input_path, output_path)
                return render_template('result.html', processed_filename=processed_filename)
            except Exception as e:
                return f"Error processing image: {str(e)}", 500
    
    # If it's a GET request, render the upload form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
