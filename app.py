from flask import Flask, request, jsonify, render_template, url_for
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
#app = Flask(__name__, static_folder='static')


# Folder configurations
UPLOAD_FOLDER = 'static/uploads'
TILE_FOLDER = 'static/image_tiles'
MOSAIC_FOLDER = 'static/mosaics'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TILE_FOLDER, exist_ok=True)
os.makedirs(MOSAIC_FOLDER, exist_ok=True)

def calculate_average_color(image):
    return np.array(image).mean(axis=(0, 1))

def find_best_match(segment_color, image_colors):
    return min(image_colors, key=lambda color: np.linalg.norm(segment_color - color[1]))

def create_mosaic(target_image_path, grid_size=(50,50)):
    # Load the target image without resizing it
    target_image = Image.open(target_image_path)
    
    # Load tile images from TILE_FOLDER
    images = [
        Image.open(os.path.join(TILE_FOLDER, img))
        for img in os.listdir(TILE_FOLDER)
        if img.endswith(('jpg', 'png', 'jpeg'))
    ]
    
    # Check if any images were loaded
    if not images:
        print("No images found in TILE_FOLDER.")
        return None

    image_colors = [(img, calculate_average_color(img)) for img in images]
    
    # Check if any colors were calculated
    if not image_colors:
        print("No colors could be calculated from tile images.")
        return None
    
    # Prepare mosaic image with the same size as the target image
    mosaic_image = Image.new('RGB', target_image.size)
    
    # Calculate the size of each tile based on the original image size and grid size
    segment_width = target_image.size[0] // grid_size[1]
    segment_height = target_image.size[1] // grid_size[0]

    for y in range(grid_size[0]):
        for x in range(grid_size[1]):
            # Crop segment from the target image
            segment = target_image.crop((x * segment_width, y * segment_height, (x + 1) * segment_width, (y + 1) * segment_height))
            segment_color = calculate_average_color(segment)
            
            # Find the best matching tile based on color
            best_match = find_best_match(segment_color, image_colors)
            # Resize the best matching tile to the segment size
            best_match_tile = best_match[0].resize((segment_width, segment_height))
            # Paste the resized tile into the mosaic image
            mosaic_image.paste(best_match_tile, (x * segment_width, y * segment_height))

    # Save the mosaic image
    mosaic_path = os.path.join(MOSAIC_FOLDER, "generated_mosaic.jpg")
    mosaic_image.save(mosaic_path)
    return mosaic_path


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save the uploaded image
    upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(upload_path)

    # Create the mosaic and get the path
    mosaic_path = create_mosaic(upload_path)

    if not mosaic_path:
        return jsonify({"error": "Failed to generate mosaic. Ensure TILE_FOLDER contains images."}), 500

    # Return the URL to the mosaic image
    return jsonify({"mosaic_url": url_for('static', filename='mosaics/generated_mosaic.jpg')})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
