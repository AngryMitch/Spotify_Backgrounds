import os

def limit_file_count(directory, max_count):
    """Limit the number of files in a directory to max_count."""
    if not os.path.exists(directory):
        os.makedirs(directory)

    # List all files in the directory, excluding directories and hidden files
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and not f.startswith('.')]
    
    # If the file count exceeds the limit, remove the oldest files
    if len(files) > max_count:
        # Sort files by modification time (oldest first)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        
        # Remove excess files
        files_to_remove = files[:len(files) - max_count]
        for file in files_to_remove:
            try:
                os.remove(os.path.join(directory, file))
                print(f"Removed file: {file}")
            except OSError as e:
                print(f"Error removing file {file}: {e}")