# Spotify Album Art Downloader and Grid Background Generator

This tool downloads album art from Spotify's cache on your computer and generates a grid background image using that artwork. Perfect for customizing your desktop background with album art from your favorite music!
If run regularly, this can be set up to be dynamic!

## Features
- **Automatic Album Art Extraction**: Retrieves album art directly from Spotify's cache.
- **Grid Background Generation**: Creates a visually appealing grid background from the extracted album art.
- **Customizable Grid Layout**: Adjust the size and spacing of the grid to suit your preferences.

## Prerequisites

- **Python 3.x**: Ensure Python is installed on your machine. [Download Python](https://www.python.org/downloads/)
- **Pillow Library**: Python Imaging Library (PIL) for image processing.
- **Spotify Cache Access**: The program requires access to Spotify's cache directory where album art is stored.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AngryMitch/Spotify_Backgrounds.git
   cd Spotify_Backgrounds
   ```

2. **Install Dependencies**

   Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file should include:
   ```
   pillow
   ```
   Install the required Python packages using premade installation files:

   **Windows**
   ```bash
   ./windows.bat
   ```
   **Linux**
   ```
   ./linux.sh
   ```

## Usage

1. **Configure Spotify Cache Path**

   By default, the program looks for Spotify’s cache in the default location. If your cache is in a different directory, specify the path in the configuration file or via command-line arguments.

2. **Run the Program**

   ```bash
   python3 scripts/__init__.py
   ```

   The script will process the album art from the Spotify cache and generate a grid background image.

3. **Customize Grid Settings**

   Open the `config.json` file to adjust grid settings such as:

   - `image_size`: Size of each album art image in the grid.
   - `spacing`: Space between images.
   - `output_resolution`: Resolution of the generated background.

   Example `config.json`:

   ```json
    {
        "GRID_WIDTH": 3,
        "GRID_HEIGHT": null,
        "IMAGE_SIZE": 1000,
        "USE_UNIQUE_NAME": false,
        "BASE_NAME": "album_art_grid",
        "FILE_ETX": ".jpg",
        "SAVE_DIR": "album_art",
        "OUTPUT_DIR": "background_images",
        "MAX_SIZE_MB": 50
    }
   ```

4. **Set as Desktop Background**

   After the script completes, you will find the generated background image in the `output` directory. Set it as your desktop wallpaper through your system settings.

## Troubleshooting

- **No Album Art Found**: Ensure Spotify is running and that you have album art cached locally. Check your Spotify cache directory and permissions.
- **Image Processing Errors**: Verify that the required Python packages are installed and up to date.

## Contributing

Feel free to submit issues, feature requests, or pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please open an issue on the [GitHub repository](https://github.com/AngryMitch/Spotify_Backgrounds/issues).

---

Thank you for using the Spotify Album Art Downloader and Grid Background Generator! Enjoy your customized desktop background!
