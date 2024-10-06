import os
from PIL import Image

def is_image_file(file_path):
    """Check if the file is an image based on its extension."""
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.file')
    return file_path.lower().endswith(image_extensions)

def find_images(directory, MIN_WIDTH=300, MIN_HEIGHT = 300):
    """Walk through the directory and find images with dimensions greater than the specified limits."""
    images = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image_file(file_path):
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        if width >= MIN_WIDTH and height >= MIN_HEIGHT:
                            print(f"{file_path} fits the criteria")
                            images.append(file_path)
                        else:
                            print(f"{file_path} is smaller than {MIN_WIDTH}x{MIN_HEIGHT}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    return images

def save_image(image_path, target_directory, file_extension='.jpeg'):
    """Save a list of images to the specified directory with the given file extension."""
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Get the original filename without the extension
            original_filename = os.path.splitext(os.path.basename(image_path))[0]
            # Define the new filename with the specified extension
            new_filename = f"{original_filename}{file_extension}"
            # Define the full path where the image will be saved
            save_path = os.path.join(target_directory, new_filename)
            # Save the image to the target directory with the new extension
            img.save(save_path)
            print(f"Saved image: {save_path}")
    except Exception as e:
        print(f"Error saving {image_path}: {e}")