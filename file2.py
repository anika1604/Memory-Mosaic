from PIL import Image
import numpy as np
import os

def calculate_average_color(image):
    return np.array(image).mean(axis=(0, 1))

def find_best_match(segment_color, image_colors):
    return min(image_colors, key=lambda color: np.linalg.norm(segment_color - color[1]))

def create_mosaic(target_image_path, image_folder, grid_size, output_path):
    target_image = Image.open(target_image_path)
    target_image = target_image.resize((grid_size[1] * 10, grid_size[0] * 10))
    
    images = [Image.open(os.path.join(image_folder, img)).resize((10, 10)) for img in os.listdir(image_folder) if img.endswith(('jpg', 'png'))]
    image_colors = [(img, calculate_average_color(img)) for img in images]
    
    mosaic_image = Image.new('RGB', target_image.size)
    segment_width, segment_height = target_image.size[0] // grid_size[1], target_image.size[1] // grid_size[0]

    for y in range(grid_size[0]):
        for x in range(grid_size[1]):
            segment = target_image.crop((x * segment_width, y * segment_height, (x + 1) * segment_width, (y + 1) * segment_height))
            segment_color = calculate_average_color(segment)
            
            best_match = find_best_match(segment_color, image_colors)
            mosaic_image.paste(best_match[0], (x * segment_width, y * segment_height))
    
    mosaic_image.save(output_path)
    print(f"Mosaic image saved to {output_path}")

# Updated paths and parameters
create_mosaic(
    target_image_path=r"C:\Users\prish\OneDrive\Desktop\target_image\th.jpeg",
    image_folder=r"C:\Users\prish\OneDrive\Desktop\image_folder",
    grid_size=(25, 25),
    output_path=r"C:\Users\prish\OneDrive\Desktop\output_path\mosaic_output.jpg"
)