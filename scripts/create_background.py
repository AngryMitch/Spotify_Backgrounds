from PIL import Image

def create_image_grid(image_paths, grid_width, grid_height, grid_image_size, final_image_size):
    """Create a grid of images based on specified grid width and height, and resize the final image to maintain aspect ratio."""
    try:
        # Calculate the total number of images that can fit in the grid
        max_images_in_grid = grid_width * grid_height
        
        # Limit the number of images to the maximum that can fit in the grid
        num_images = min(len(image_paths), max_images_in_grid)
        
        # Calculate the number of rows needed based on the grid height
        num_rows = (num_images + grid_width - 1) // grid_width
        
        # Calculate the total height of the grid image based on the number of rows
        total_height = min(num_rows, grid_height) * grid_image_size
        
        # Create a new image for the grid
        grid_image = Image.new('RGB', (grid_width * grid_image_size, total_height))
        
        for index in range(num_images):
            image_path = image_paths[index]
            try:
                img = Image.open(image_path).resize((grid_image_size, grid_image_size))
                x = (index % grid_width) * grid_image_size
                y = (index // grid_width) * grid_image_size
                grid_image.paste(img, (x, y))
            except Exception as e:
                print(f"Error processing image '{image_path}': {e}")
        
        # Calculate the new dimensions while maintaining the aspect ratio
        aspect_ratio = grid_image.width / grid_image.height
        new_height = final_image_size  # Desired final height
        new_width = int(new_height * aspect_ratio)

        # Resize the final image
        final_image = grid_image.resize((new_width, new_height), Image.LANCZOS)

        return final_image

    except Exception as e:
        print(f"Error creating image grid: {e}")
        return None
