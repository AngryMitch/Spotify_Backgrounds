### =============================================
### === Imports =================================
### =============================================
# === System Imports ============================
import os, json, time

# === Custom Imports ============================
from scripts.valid_inputs import validate_and_adjust_config, ensure_directory_exists, get_cache_directories
from scripts.grab_images import find_images, save_image
from scripts.create_background import create_image_grid
from scripts.file_management import limit_file_count


### =============================================
### === Variables ===============================
### =============================================
# Default configuration values
default_config = {
    "GRID_WIDTH": 4,
    "GRID_HEIGHT": 4,
    "FINAL_IMAGE_SIZE_PX": 3000,
    "ALBUM_IMAGE_SIZE_PX": 500,
    "USE_UNIQUE_NAME": False,
    "BASE_NAME": "background_art",
    "FILE_ETX": ".jpg",
    "SAVE_DIR": "album_art",
    "OUTPUT_DIR": "background_images",
    "CACHE_DIR": [""],
    "USE_DEFAULT_CACHE": True,
    "MAX_IMAGE_COUNT_ALBUM": 50,
    "MAX_IMAGE_COUNT_BACKGROUND": 3
}

# Get the absolute path to the config file
config_file_path = os.path.abspath('config.json')

# Function to load the configuration
def load_config(filepath):
    if not os.path.exists(filepath):
        print(f"Config file not found. Creating new one at: {filepath}")
        # If the config file doesn't exist, create it with default values
        with open(filepath, 'w') as file:
            json.dump(default_config, file, indent=4)
    
    # Load the configuration from file
    with open(filepath, 'r') as file:
        return json.load(file)
    
# Load the configuration from the file
config = load_config(config_file_path)

# Validate and adjust the loaded configuration
validation_errors = validate_and_adjust_config(config)

# Handle validation results
if validation_errors:
    for error in validation_errors:
        raise TypeError(f"Configuration error(s): {error}")
else:
    print("Configuration is valid.")

# Assign the JSON config properties to variables
GRID_WIDTH = config.get('GRID_WIDTH')
GRID_HEIGHT = config.get('GRID_HEIGHT')
FINAL_IMAGE_SIZE_PX = config.get('FINAL_IMAGE_SIZE_PX')
ALBUM_IMAGE_SIZE_PX = config.get('ALBUM_IMAGE_SIZE_PX')
USE_UNIQUE_NAME = config.get('USE_UNIQUE_NAME')
BASE_NAME = config.get('BASE_NAME')
FILE_ETX = config.get('FILE_ETX')
SAVE_DIR = os.path.join(os.curdir, config.get('SAVE_DIR'))
OUTPUT_DIR = os.path.join(os.curdir, config.get('OUTPUT_DIR'))
CACHE_DIR = config.get('CACHE_DIR')
USE_DEFAULT_CACHE = config.get('USE_DEFAULT_CACHE')
MAX_IMAGE_COUNT_ALBUM = config.get('MAX_IMAGE_COUNT_ALBUM')
MAX_IMAGE_COUNT_BACKGROUND = config.get('MAX_IMAGE_COUNT_BACKGROUND')

### =============================================
### === Main Program ============================
### =============================================
if __name__ == "__main__":
    # --- Ensure the directories exist --------------
    ensure_directory_exists(SAVE_DIR)                   # Ensure Album Art Directory exists, else make
    ensure_directory_exists(OUTPUT_DIR)                 # Ensure Background Directory exists, else make

    if USE_DEFAULT_CACHE:
        """Assign the default cache if setting valid"""
        CACHE_DIR = get_cache_directories()

    for directory in CACHE_DIR:
        """Ensure the cache directories exist"""
        ensure_directory_exists(directory)
        print (directory)
    
    # --- Grab Images from Cache and Save to SAVE_DIR -----------
    all_images = []                                     # Array of all Images
    MIN_WIDTH = 500                                     # OPTIONAL (default is 500px): Minimum sizes in pixels
    MIN_HEIGHT = 500
    
    for directory in CACHE_DIR:
        """ Loop through directory and assign valid image paths to array """
        images = find_images(directory, MIN_WIDTH, MIN_HEIGHT)  # To change minimum, update function to be find_images(directory, MIN_WIDTH, MIN_HEIGHT)
        all_images.extend(images)
    
    for image in all_images:
        """ Loop through image path array and save into given directory """
        save_image(image, SAVE_DIR, FILE_ETX)
    
    # If images assigned successfully, print the count and where they were saved
    if all_images:
        print (f"Found {len(all_images)} images and saved successfully in {SAVE_DIR}")
        
    # --- Limit the file sizes in each directory --------
    limit_file_count(SAVE_DIR, MAX_IMAGE_COUNT_ALBUM)
    limit_file_count(OUTPUT_DIR, MAX_IMAGE_COUNT_BACKGROUND)
    
    
    image_paths = []
    
    try:
        # List all files in the directory
        for filename in os.listdir(SAVE_DIR):
            # Get the file extension
            ext = os.path.splitext(filename)[1].lower()
            image_paths.append(os.path.join(SAVE_DIR, filename))
    except Exception as e:
        print(f"Error accessing directory '{SAVE_DIR}': {e}")
            
    # --- Create the grid background from the album art -----------
    if USE_UNIQUE_NAME:
        """ Check for and apply unique time based index"""
        unique_suffix = int(time.time())  # Using timestamp as a unique identifier
        BASE_NAME += f"_{unique_suffix}"    
    
    try:  # Create Image grid from all_images array
        grid_image = create_image_grid(image_paths, GRID_WIDTH, GRID_HEIGHT, ALBUM_IMAGE_SIZE_PX, FINAL_IMAGE_SIZE_PX)
        output_file_path = os.path.join(OUTPUT_DIR, f"{BASE_NAME}{FILE_ETX}")
        grid_image.save(output_file_path)
        print(f"Successfully saved image @ {output_file_path}")
    except Exception as e:
        print(f"Error creating background image: {e}")