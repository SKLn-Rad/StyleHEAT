import os
import shutil
from PIL import Image
import logging

def adjust_point(x, y, z, original_size, new_size, crop_box):
    """Adjust a point's coordinates after resizing and cropping an image."""
    original_width, original_height = original_size
    new_width, new_height = new_size
    left, top, right, bottom = crop_box

    # Adjust the point for resizing
    x_ratio = new_width / original_width
    y_ratio = new_height / original_height
    z_ratio = x_ratio  # Assuming z scales similarly to x

    x *= x_ratio
    y *= y_ratio
    z *= z_ratio

    # Adjust the point for cropping
    x -= left
    y -= top
    # No need to adjust z as it doesn't correspond to any physical coordinate in 2D space

    return x, y, z

def resize_and_crop(image, size):
    """Resize and crop an image to fit the specified size."""
    # Image size
    img_width, img_height = image.size

    # Calculate the target width and height to preserve the aspect ratio
    if img_width > img_height:
        width = size * img_width // img_height
        height = size
    else:
        width = size
        height = size * img_height // img_width

    # Resize while maintaining the aspect ratio
    image = image.resize((width, height), Image.ANTIALIAS)

    # Calculate coordinates for center crop
    left = (width - size) / 2
    top = (height - size) / 2
    right = (width + size) / 2
    bottom = (height + size) / 2

    # Crop the center of the image
    image = image.crop((left, top, right, bottom))

    return image

def resize_images(input_folder, output_folder):
    logging.basicConfig(level=logging.INFO)

    if os.path.exists(output_folder):
        logging.warning("Output folder '{}' already exists. Deleting it.".format(output_folder))
        shutil.rmtree(output_folder)
    
    os.makedirs(output_folder)

    # Get all the image files in the input folder recursively
    image_files = [os.path.join(dirpath, filename) 
                   for dirpath, dirnames, filenames in os.walk(input_folder) 
                   for filename in filenames 
                   if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    total_images = len(image_files)
    
    for index, path in enumerate(image_files, start=1):
        logging.info("Resizing {} of {} images".format(index, total_images))
        
        try:
            with Image.open(path) as image:
                image = resize_and_crop(image, 1024)

                # Zoom in 20% on the face
                width, height = image.size
                left = width * 0.1
                top = height * 0.1
                right = width * 0.9
                bottom = height * 0.9
                image = image.crop((left, top, right, bottom))

                # Construct the output path but change the extension to .jpeg
                relative_path = os.path.relpath(path, input_folder)
                output_path_noext, _ = os.path.splitext(os.path.join(output_folder, relative_path))
                output_path = output_path_noext + ".jpeg"
                
                # Create output directories if they don't exist
                output_dir = os.path.dirname(output_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                # Save the image in JPEG format
                image.save(output_path, 'JPEG', quality=100, optimize=True, progressive=True)
                
                logging.info("Resized {} of {} images".format(index, total_images))
        except Exception as e:
            logging.error("Error processing file {}: {}".format(path, e))

if __name__ == "__main__":
    input_folder = "robotimages"
    output_folder = "robotimages_resized"
    resize_images(input_folder, output_folder)
