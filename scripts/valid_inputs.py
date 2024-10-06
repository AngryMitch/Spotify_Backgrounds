### =============================================
### === Input Validation ========================
### =============================================
import os, platform

# Function to validate and adjust configuration values
def validate_and_adjust_config(config):
    errors = []
    
    # Validate GRID_WIDTH and GRID_HEIGHT
    grid_width = config.get('GRID_WIDTH')
    grid_height = config.get('GRID_HEIGHT')
    
    if grid_width is None and grid_height is None:
        errors.append("Both GRID_WIDTH and GRID_HEIGHT cannot be null.")
    elif grid_width is None:
        config['GRID_WIDTH'] = grid_height  # Assign the same value
    elif grid_height is None:
        config['GRID_HEIGHT'] = grid_width  # Assign the same value
    elif not isinstance(grid_width, int) or grid_width <= 0:
        errors.append("GRID_WIDTH must be a positive integer.")
    elif not isinstance(grid_height, int) or grid_height <= 0:
        errors.append("GRID_HEIGHT must be a positive integer.")
    
    # Validate FINAL_IMAGE_SIZE_PX
    if not isinstance(config.get('FINAL_IMAGE_SIZE_PX'), int) or config['FINAL_IMAGE_SIZE_PX'] <= 0:
        errors.append("FINAL_IMAGE_SIZE_PX must be a positive integer.")
        
    # Validate FINAL_IMAGE_SIZE_PX
    if not isinstance(config.get('ALBUM_IMAGE_SIZE_PX'), int) or config['FINAL_IMAGE_SIZE_PX'] <= 0:
        errors.append("ALBUM_IMAGE_SIZE_PX must be a positive integer.")
    
    # Validate USE_UNIQUE_NAME
    if not isinstance(config.get('USE_UNIQUE_NAME'), bool):
        errors.append("USE_UNIQUE_NAME must be a boolean value.")
    
    # Validate BASE_NAME
    if not isinstance(config.get('BASE_NAME'), str) or not config['BASE_NAME']:
        errors.append("BASE_NAME must be a non-empty string.")
    
    # Validate FILE_ETX
    if not isinstance(config.get('FILE_ETX'), str) or not config['FILE_ETX'].startswith('.'):
        errors.append("FILE_ETX must be a string starting with a dot (e.g. .jpg).")
    
    # Validate SAVE_DIR and OUTPUT_DIR
    for dir_name in ['SAVE_DIR', 'OUTPUT_DIR']:
        if not isinstance(config.get(dir_name), str) or not config[dir_name]:
            errors.append(f"{dir_name} must be a non-empty string.")
    
    # Validate CACHE_DIR
    if not isinstance(config.get('CACHE_DIR'), list) or any(not isinstance(item, str) for item in config['CACHE_DIR']):
        errors.append("CACHE_DIR must be a list of strings.")
    
    # Validate USE_DEFAULT_CACHE
    if not isinstance(config.get('USE_DEFAULT_CACHE'), bool):
        errors.append("USE_DEFAULT_CACHE must be a boolean value.")
    
    # Validate MAX_IMAGE_COUNT_ALBUM
    if not isinstance(config.get('MAX_IMAGE_COUNT_ALBUM'), int) or config['MAX_IMAGE_COUNT_ALBUM'] < 0:
        errors.append("MAX_IMAGE_COUNT_ALBUM must be a non-negative integer.")
    
    # Validate MAX_IMAGE_COUNT_BACKGROUND
    if not isinstance(config.get('MAX_IMAGE_COUNT_BACKGROUND'), int) or config['MAX_IMAGE_COUNT_BACKGROUND'] < 0:
        errors.append("MAX_IMAGE_COUNT_BACKGROUND must be a non-negative integer.")
    
    
    return errors

def ensure_directory_exists(directory):
    """Check if a directory exists in the current folder, and create it if it does not."""
    current_directory = os.getcwd()  # Get the current working directory
    absolute_directory = os.path.abspath(directory)  # Get the absolute path of the provided directory
    isInCurrentDirectory = True
    
    # Check if the directory is within the current working directory
    if not absolute_directory.startswith(current_directory):
        isInCurrentDirectory = False
        
    # Check if the directory exists and create it if is within the current directory and it does not exist
    if not os.path.exists(directory) and isInCurrentDirectory:
        os.makedirs(directory)
        print(f"Directory did not exist. Directory created: {directory}")
    elif not os.path.exists(directory) and isInCurrentDirectory == False:
        print(f"Directory did not exist. Please ensure the Supplied Directory '{directory}' exists.")
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