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

1. *****Clone the Repository**

   ```bash
   git clone https://github.com/AngryMitch/Spotify_Backgrounds.git
   cd Spotify_Backgrounds
   ```
   (Or [download](https://github.com/AngryMitch/Spotify_Backgrounds/archive/refs/heads/main.zip) the zip and unpack)

2. **Install Dependencies**

   Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file should include:
   ```
   10.4.0 pillow
   ```
**OR you can run the executables**

## Usage
1. **Configure Spotify Cache Path**

   By default, the program looks for Spotify’s cache in the default location. If your cache is in a different directory, or you want to scrape for images elswhere specify the path in the configuration file or via command-line arguments.

2. **Run the Program**

   ```bash
   python3 main.py
   ```

   **OR you can run the executables**

   The script will process the album art from the Spotify cache and generate a grid with those images.

3. **Customize Grid Settings**
   NOTE: May raise errors but set config option to null if empty (e.g. { ... `GRID_WIDTH`: 0, `GRID_HEIGHT`: 5 ... }

   Open the `config.json` file to adjust grid settings such as:

   - `GRID_WIDTH`: The set size of width of the grid (Note: leave null for square image using GRID_HEIGHT)
   - `GRID_HEIGHT`: The set size of height of the grid (Note: leave null for square image using GRID_WIDTH)
   - `FINAL_IMAGE_SIZE_PX`: Resolution (px) of the generated background.
   -`ALBUM_IMAGE_SIZE_PX`: The resolution (px) of the album art it builds the background with.
   - `USE_UNIQUE_NAME`: true or false, this will generate an index for the file name allowing for slideshow backgrounds.
   - `BASE_NAME`: What the name of the file you would like saved is.
   - `FILE_ETX`: What file extension you want it saved as.
   - `SAVE_DIR`: The name of where the album art is saved.
   - `OUTPUT_DIR`: The name of Background Directory
   - `CACHE_DIR`: Specific Directorys, basically becomes an folder image crawler
   - `USE_DEFAULT_CACHE`: True or False, it can find the default directory for Spotify on Linux and Windows OS's
   - `MAX_IMAGE_COUNT_ALBUM`: Limits the size of the SAVE_DIR
   - `MAX_IMAGE_COUNT_ALBUM`: Limits the size of the OUTPUT_DIR
   
   Example `config.json`:
   ```json
   {
      "GRID_WIDTH": 4,
      "GRID_HEIGHT": 4,
      "FINAL_IMAGE_SIZE_PX": 1200,
      "ALBUM_IMAGE_SIZE_PX": 600,
      "USE_UNIQUE_NAME": false,
      "BASE_NAME": "background_art",
      "FILE_ETX": ".jpg",
      "SAVE_DIR": "album_art",
      "OUTPUT_DIR": "background_images",
      "CACHE_DIR": [""],
      "USE_DEFAULT_CACHE": true,
      "MAX_IMAGE_COUNT_ALBUM": 24,
      "MAX_IMAGE_COUNT_BACKGROUND": 3
   }
   ```

5. **Set as Desktop Background**

   After the script completes, you will find the generated background image in the `OUTPUT_DIR` directory within the project. Set it as your desktop wallpaper through your system settings.

## Troubleshooting

- **No Album Art Found**: Ensure Spotify is running and that you have album art cached locally. Check your Spotify cache directory and permissions.

## Contributing

Feel free to submit issues, feature requests, or pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/AngryMitch/Spotify_Backgrounds/blob/main/.github/LICENSE.md) file for details.

## Contact

For any questions or support, please open an issue on the [GitHub repository](https://github.com/AngryMitch/Spotify_Backgrounds/issues).

---

Thank you for using the Spotify Album Art Downloader and Grid Background Generator! Enjoy your customized desktop background!
