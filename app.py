from flask import Flask, request, send_file, render_template
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"no_bg_{os.path.splitext(file.filename)[0]}.png")
        input_image = Image.open(filepath)
        output_image = remove(input_image)

        # Convert to RGBA to ensure we can save it as PNG
        if output_image.mode != 'RGBA':
            output_image = output_image.convert('RGBA')

        output_image.save(output_path, format='PNG')

        return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
