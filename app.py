from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from tools.rembg_tool import remove_background  # Import your custom background removal tool

app = Flask(__name__)

# Configuration for file upload and processed image directories
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create necessary directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Check if a file's extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to upload and process an image
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # Validate file and process it if valid
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            # Generate processed file path
            processed_filename = 'processed_' + filename
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            
            # Use the remove_background function
            try:
                remove_background(input_path, output_path)
                return render_template('result.html', processed_filename=processed_filename)
            except Exception as e:
                return f"Error processing image: {str(e)}", 500
    
    # Render the upload form for GET requests
    return render_template('index.html')

if __name__ == '__main__':
    # Use Render's PORT environment variable for deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
