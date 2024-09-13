import os
from PIL import Image

# Define the directories for images and output
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'album_art')
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'background_images')

# List of directories to manage
dir_list = [input_dir, output_dir]

# Default presets
DEFAULT_MAX_FOLDER_SIZE_MB = 5  # Maximum folder size in megabytes
DEFAULT_MAX_FILE_COUNT = 100    # Maximum number of files in a directory

def get_total_size(directory):
    """
    Calculates the total size of all files in the given directory.

    Parameters:
        directory (str): The directory to check.

    Returns:
        int: Total size of all files in bytes.
    """
    total_size = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            total_size += os.path.getsize(file_path)
    return total_size

def remove_oldest_files(directory, max_size_mb=DEFAULT_MAX_FOLDER_SIZE_MB, max_file_count=DEFAULT_MAX_FILE_COUNT):
    """
    Ensures the folder size and file count do not exceed the specified limits by removing the oldest files.

    Parameters:
        directory (str): The directory to manage.
        max_size_mb (int): The maximum allowed folder size in megabytes (default is 5 MB).
        max_file_count (int): The maximum number of files allowed in the directory (default is 100).
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    total_size_bytes = get_total_size(directory)
    if total_size_bytes <= max_size_bytes and len(os.listdir(directory)) <= max_file_count:
        print(f"Folder {directory} is within size and file count limits.")
        return

    # Get list of files with their modification times
    files = [(os.path.join(directory, f), os.path.getmtime(os.path.join(directory, f))) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # Sort files by modification time (oldest first)
    files.sort(key=lambda x: x[1])

    # Track removed size
    removed_size_bytes = 0

    # Remove files to meet size and file count requirements
    while (total_size_bytes > max_size_bytes or len(os.listdir(directory)) > max_file_count) and files:
        file_path, _ = files.pop(0)
        file_size_bytes = os.path.getsize(file_path)
        os.remove(file_path)
        removed_size_bytes += file_size_bytes
        total_size_bytes -= file_size_bytes
        print(f"Removed file: {file_path}. Total removed size: {removed_size_bytes / (1024 * 1024):.2f} MB")

def edit_files(max_folder_size_mb=DEFAULT_MAX_FOLDER_SIZE_MB, max_file_count=DEFAULT_MAX_FILE_COUNT):
    """
    Edits files in the specified directories to ensure their sizes and file counts do not exceed the given limits.

    Parameters:
        max_folder_size_mb (int): The maximum allowed folder size in megabytes (default is 5 MB).
        max_file_count (int): The maximum number of files allowed in each directory (default is 100).
    """
    for directory in dir_list:
        remove_oldest_files(directory, max_folder_size_mb, max_file_count)

def resize_images(file_size):
    for filename in os.listdir(output_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(output_dir, filename)
            with Image.open(img_path) as img:
                width, height = img.size
                
                # Calculate new dimensions
                aspect_ratio = width / height
                new_width = file_size
                new_height = int(file_size / aspect_ratio)
                
                # Resize image
                resized_image = img.resize((new_width, new_height), Image.ANTIALIAS)
                resized_image.save(img_path)

if __name__ == "__main__":
    edit_files()
