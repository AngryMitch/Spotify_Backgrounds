import os
from PIL import Image
import math

def create_image_grid(images, grid_size, image_size):
    """Create a grid of images."""
    grid_width, grid_height = grid_size
    grid_image = Image.new('RGB', (grid_width * image_size, grid_height * image_size))

    for index, image in enumerate(images):
        x = (index % grid_width) * image_size
        y = (index // grid_width) * image_size
        grid_image.paste(image, (x, y))

    return grid_image

def resize_images(output_dir, max_size):
    for filename in os.listdir(output_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(output_dir, filename)
            with Image.open(img_path) as img:
                # Get original dimensions
                original_width, original_height = img.size
                
                # Calculate the new dimensions while preserving aspect ratio
                if original_width > original_height:
                    new_width = max_size
                    new_height = int((max_size / original_width) * original_height)
                else:
                    new_height = max_size
                    new_width = int((max_size / original_height) * original_width)
                
                # Resize image
                resized_image = img.resize((new_width, new_height), Image.LANCZOS)
                
                # Save the resized image
                resized_image.save(img_path)

def generate_grid(grid_width=5, grid_height=None, image_size=200, output_filename='album_art_grid.jpg', input_dir='album_art', output_dir='background_images'):
    """Generate a grid of images and save it with specified dimensions and filename."""
    # Ensure the directories exists
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # If only one input, make Square
    if grid_height == None and grid_width != None:
        grid_height = grid_width
    elif grid_width == None and grid_height != None:
        grid_width = grid_height
    elif grid_width == None and grid_height == None:
        print ("Please enter valid value")
        return

    # Ensure Grid not too big
    max_num = 200
    if grid_width > max_num or grid_height > max_num:
        print(f"Grid too large, generating grid of {max_num} x {max_num} (max), increase max @ line 48 create_background.py")
        grid_width = max_num
        grid_height = max_num

    print(f"Generating Grid with - Grid: {grid_width}x{grid_height},    Image Size: {image_size}")

    # Load images
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.jpg')]
    if not image_files:
        print("No images found in the directory.")
        return

    # Ensure Uniform Size
    images = []
    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        with Image.open(image_path) as img:
            # Resize image to ensure uniform size
            img = img.resize((image_size, image_size))
            images.append(img)

    num_images = len(images)

    # Determine grid size if not provided
    count_diff = (grid_width * grid_height) - num_images
    isSquare = grid_width == grid_height

    if grid_width is None or grid_height is None:
        # Default to a square grid if no dimensions are provided
        grid_width = grid_height = int(math.ceil(math.sqrt(num_images)))
    elif count_diff <= 0:
        # Check if the requested grid is smaller than the number of images
        pass
    else:
        # Ensure grid size is not too large
        subtract = 1
        if count_diff > 0:
            print(f"Not enough images for requested grid size, downsizing to fit")
        while count_diff > 0:
            # Bring grid size down to fit
            print(count_diff)
            if count_diff >= 1000:
                subtract = 10
            elif count_diff >= 100:
                subtract = 3
            elif count_diff >= 10:
                subtract = 1
            if grid_width >= grid_height:
                grid_width -= subtract
            else:
                grid_height -= subtract
            count_diff = (grid_width * grid_height) - num_images  # Recalculate count
        # If it was square, ensure it remains square
        if isSquare and grid_width != grid_height:
            if grid_width > grid_height:
                grid_width -= 1
            else:
                grid_height -= 1

    # Debugging: Print grid dimensions and number of images
    print(f"Requested Grid Size: {grid_width}x{grid_height} for a grid space of {grid_width * grid_height}")
    print(f"Number of Images: {num_images}, which means {num_images - (grid_width * grid_height)} images were not used")

    # Create and save the grid image
    grid_image = create_image_grid(images, (grid_width, grid_height), image_size)
    output_image_path = os.path.join(output_dir, output_filename)
    grid_image.save(output_image_path)
    print(f"Grid image saved to {output_image_path}")

if __name__ == "__main__":
    # Example usage with default values
    generate_grid(grid_width=5, grid_height=5, output_filename="album_art_grid.jpg", image_size=400, input_dir='album_art', output_dir='background_images')
