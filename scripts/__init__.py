# System Imports
import os
import re
import platform
import json

# Custom imports
from parse_for_images import search_and_process_images
from create_background import generate_grid, resize_images
from manage_files import edit_files

### =============================================
### === Variables ===============================
### =============================================
# Load configuration from JSON file
def load_config(file_path):
    """Load configuration from a JSON file."""
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

# Load the configuration
config = load_config('config.json')

# Constants from configuration
GRID_WIDTH = config.get('GRID_WIDTH')
GRID_HEIGHT = config.get('GRID_HEIGHT')
IMAGE_SIZE = config.get('IMAGE_SIZE')
USE_UNIQUE_NAME = config.get('USE_UNIQUE_NAME')
BASE_NAME = config.get('BASE_NAME')
FILE_ETX = config.get('FILE_ETX')
SAVE_DIR = os.path.join(os.curdir, config.get('SAVE_DIR'))
OUTPUT_DIR = os.path.join(os.curdir, config.get('OUTPUT_DIR'))
CACHE_DIR = config.get('CACHE_DIR')
USE_DEFAULT_CACHE = config.get('USE_DEFAULT_CACHE')
MAX_SIZE_MB = config.get('MAX_SIZE_MB')


### =============================================
### === Input Validation ========================
### =============================================
# List of variables to check
variables = {
    "GRID_WIDTH": GRID_WIDTH,
    "GRID_HEIGHT": GRID_HEIGHT,
    "IMAGE_SIZE": IMAGE_SIZE,
    "USE_UNIQUE_NAME": USE_UNIQUE_NAME,
    "BASE_NAME": BASE_NAME,
    "FILE_ETX": FILE_ETX,
    "SAVE_DIR": SAVE_DIR,
    "OUTPUT_DIR": OUTPUT_DIR,
    "CACHE_DIR": CACHE_DIR,
    "USE_DEFAULT_CACHE": USE_DEFAULT_CACHE,
    "MAX_SIZE_MB": MAX_SIZE_MB,
}

# Collect missing variables and their types
missing_vars = []
for var_name, var_value in variables.items(): # Checks for null values
    if var_value is None:
        missing_vars.append(f"{var_name} (type: {type(var_value).__name__})")

# Check if FILE_ETX is one of the allowed extensions
allowed_extensions = {'.png', '.jpg', '.jpeg'}
if FILE_ETX not in allowed_extensions:
    raise Exception(f"Invalid file extension '{FILE_ETX}'. Ensure it matches one of the following: {', '.join(allowed_extensions)}")

# Confirm at least one grid dimension is set
if GRID_WIDTH is None and GRID_HEIGHT is None:
    raise Exception("Please set at least one dimension for the image grid. (Note: Setting one dimension will create a square grid)")

# Check for Cache Directory
if not USE_DEFAULT_CACHE:
    if CACHE_DIR is None or len(CACHE_DIR) == 0:
        raise Exception("Please use the default cache or set directory paths in CACHE_DIR as a list of strings.")

### =============================================
### === Functions ===============================
### =============================================
# Determine if the directories exist, if not create them
def ensure_directory_exists(directory):
    """Check if a directory exists and create it if it does not."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory created: {directory}")
    else:
        print(f"Directory already exists: {directory}")

# Determine the operating system and set the cache directories accordingly
def get_cache_directories():
    """
    Checks Operating System and updates filepath occordingly
    Raises:
        OSError: Unsupported operating system
    Returns:
        Array: Returns an array of paths to collect images from
    """
    os_type = platform.system()  # Returns 'Linux', 'Windows', etc.

    # Check for Platform type and return relevant directories
    if os_type == 'Windows':
        localappdata_path = os.getenv('LOCALAPPDATA')  # LocalAppData Directory for Windows systems
        if not localappdata_path:
            raise EnvironmentError("LOCALAPPDATA environment variable not set.")
        
        spotify_base_path = os.path.join(localappdata_path, 'Spotify')
        
        # Check if the Spotify directory exists
        if not os.path.isdir(spotify_base_path):
            raise FileNotFoundError(f"The path {spotify_base_path} does not exist.")
        
        # Construct paths for Data and Storage
        data_path = os.path.join(spotify_base_path, 'Data')
        storage_path = os.path.join(spotify_base_path, 'Storage')

        # Verify that these directories exist
        if not os.path.isdir(data_path):
            raise FileNotFoundError(f"The path {data_path} does not exist.")
        if not os.path.isdir(storage_path):
            raise FileNotFoundError(f"The path {storage_path} does not exist.")

        return [data_path, storage_path]
    elif os_type == 'Linux':
        HOME_DIR = os.path.expanduser("~")                  # Home Directory for Unix systems
        return [
            os.path.join(HOME_DIR, '.cache', 'spotify', 'Data'),
            os.path.join(HOME_DIR, '.cache', 'spotify', 'Storage')
        ]
    else:
        raise OSError(f"Unsupported operating system: {os_type}")
# Check if using default cache directories
if(USE_DEFAULT_CACHE == True): 
    CACHE_DIR = get_cache_directories()

# Function to generate a unique background name
def generate_unique_background_name(base_name, extension):
    """
    Counts files and generates a unqiue id (count + 1) for file
    Args:
        base_name (_type_): base file name
        extension (_type_): file extension

    Returns:
        file_name : returns new file name for background file
    """
    # Pattern to match existing files with the same base name and a number
    pattern = re.compile(rf"^{re.escape(base_name)}_(\d*){re.escape(extension)}$")
    files = os.listdir(OUTPUT_DIR)
    max_number = 0

    # Check existing files in the directory
    for file in files:
        match = pattern.match(file)
        if match:
            number = match.group(1)
            if number:
                max_number = max(max_number, int(number))

    # Increment the number for the new file name
    new_number = max_number + 1
    new_name = f"{base_name}_{new_number}{extension}"
    
    return new_name

# Fucntion to return indexed name
def return_name():
    """
    Checks if creating unique id or not and sets BACKGROUND_NAME variable accordingly
    Returns:
        file name: returns file name of newly generated background (before generation)
    """
    # Generate a unique background name if the option is enabled
    if USE_UNIQUE_NAME:
        BACKGROUND_NAME = generate_unique_background_name(BASE_NAME, FILE_ETX)
    else:
        BACKGROUND_NAME = f"{BASE_NAME}{FILE_ETX}"

    return BACKGROUND_NAME

### =============================================
### === Programs ================================
### =============================================
# Ensure the directories exist
ensure_directory_exists(SAVE_DIR)
ensure_directory_exists(OUTPUT_DIR)

# Find files from Spotify and save them
search_and_process_images(CACHE_DIR, SAVE_DIR)

# Generate Grid Background with saved images
generate_grid(GRID_WIDTH, GRID_HEIGHT, IMAGE_SIZE, return_name(), SAVE_DIR, OUTPUT_DIR)

# Manage files to make sure program doesnt bloat, deletes oldest after reaching file size
edit_files(MAX_SIZE_MB)

# Resize grid images to defined size
resize_images(OUTPUT_DIR, IMAGE_SIZE)
