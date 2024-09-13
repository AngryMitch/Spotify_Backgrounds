import os
import hashlib
from PIL import Image

# Define the directories to search and the output directory
home_dir = os.path.expanduser("~")
curr_dir = os.path.dirname(os.path.abspath(__file__))

# File to store processed image hashes
hashes_file = os.path.join(curr_dir, 'processed_hashes.txt')

# Load existing hashes from the file
if os.path.exists(hashes_file):
    with open(hashes_file, 'r') as f:
        processed_hashes = set(line.strip() for line in f)
else:
    processed_hashes = set()

def get_image_hash(image_path):
    """Generate a hash for the image content."""
    hasher = hashlib.md5()
    try:
        with open(image_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
    except Exception as e:
        print(f"Error hashing {image_path}: {e}")
        return None
    return hasher.hexdigest()

def process_image(image_path, output_path):
    """Process the image, convert to .jpg and save it if not a duplicate."""
    image_hash = get_image_hash(image_path)
    if image_hash is None:
        return

    if image_hash in processed_hashes:
        print(f"Skipped (duplicate): {image_path}")
        return

    try:
        with Image.open(image_path) as img:
            # Check if the image is larger than 400px in either dimension
            if img.width > 400 or img.height > 400:
                # Convert and save as .jpg
                img.convert('RGB').save(output_path, 'JPEG')
                processed_hashes.add(image_hash)
                # Save the hash to the file
                with open(hashes_file, 'a') as f:
                    f.write(f"{image_hash}\n")
                print(f"Processed and saved: {output_path}")
            else:
                print(f"Skipped (not large enough): {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def search_and_process_images(cache_dirs, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Loop through target directories and search for files
    for directory in cache_dirs:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.file'):  # Check for .file images
                    image_path = os.path.join(root, file)
                    output_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.jpg")
                    process_image(image_path, output_path)

cache_dirs = [
    os.path.join(home_dir, '.cache', 'spotify', 'Data'),
    os.path.join(home_dir, '.cache', 'spotify', 'Storage')
]

if __name__ == "__main__":
    search_and_process_images(cache_dirs)
