# System Imports
import os
import re
import platform

# Custom imports
from parse_for_images import search_and_process_images
from create_background import generate_grid, resize_images
from manage_files import edit_files

GRID_WIDTH = None               # Is /image, Set to 200 for maximum grid size. Only 1 value needed (makes square) set to None
GRID_HEIGHT = 6                 # Is /image, Set to 200 for maximum grid size. Only 1 value needed (makes square) set to None
IMAGE_SIZE = 1000               # Sets image pixel size

# Define the file name and type
USE_UNIQUE_NAME = False          # Option to enable unique background naming is True or False
BASE_NAME = "album_art_grid"    # Define the base name and extension
FILE_ETX = ".jpg"               # Define the extension (note: needs to start with '.' and be a supported image extenstion (e.g. .png, .jpg, etc.))

# Define the directories to search and the output directory
SAVE_DIR = os.path.join(os.curdir, 'album_art')             # Output directory for album art
OUTPUT_DIR = os.path.join(os.curdir, 'background_images')   # Output directory for background images
MAX_SIZE_MB = 50 # MB                                       # Maximum folder sizes in MB

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
        appdata_path = os.getenv('APPDATA')                     # AppData Directory for Windows systems
        spotify_folder = re.compile(r'SpotifyAB\.SpotifyMusic_\w+')    # Define the regex pattern for matching the Spotify path
        if not appdata_path:
            raise EnvironmentError("APPDATA environment variable not set.")
        return [
            os.path.join(appdata_path, 'Local', 'Packages', spotify_folder, 'LocalCache', 'Spotify', 'Data'),
            os.path.join(appdata_path, 'Local', 'Packages', spotify_folder, 'LocalState', 'Spotify', 'Storage')
        ]
    elif os_type == 'Linux':
        HOME_DIR = os.path.expanduser("~")                  # Home Directory for Unix systems
        return [
            os.path.join(HOME_DIR, '.cache', 'spotify', 'Data'),
            os.path.join(HOME_DIR, '.cache', 'spotify', 'Storage')
        ]
    else:
        raise OSError(f"Unsupported operating system: {os_type}")
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


# Ensure the directories exist
ensure_directory_exists(SAVE_DIR)
ensure_directory_exists(OUTPUT_DIR)

# Find files from Spotify and save them
search_and_process_images(CACHE_DIR, SAVE_DIR)

# Generate Grid Background with saved images
generate_grid(GRID_WIDTH, GRID_HEIGHT, IMAGE_SIZE, return_name(), OUTPUT_DIR)

# Manage files to make sure program doesnt bloat, deletes oldest after reaching file size
edit_files(MAX_SIZE_MB)

# Resize grid images to defined size
resize_images(OUTPUT_DIR, IMAGE_SIZE)
