# Manga to Comics Converter
This Python 3 script converts manga pages into Western comic-style pages by reversing the reading direction, among other transformations.

## Installation
First, clone the repository or download the files to your local machine.

Before running the script, you need to install the required Python libraries. If you have CUDA available and wish to leverage GPU acceleration, you should specify a custom index URL when installing the packages. Otherwise, use the standard installation command. 

### Standard Installation
```bash
pip install -r requirements.txt
```

## Installation with CUDA
If you have CUDA installed and want to use GPU capabilities, append the --index-url option with the appropriate URL for CUDA-optimized packages:

```bash
pip install --index-url https://download.pytorch.org/whl/cu121 -r requirements.txt
```

PS: I don't have a device with CUDA myself, but this should technically work. Try it and let me know.

## Usage
To use the script, you need to specify the source directory (or file) containing the manga images, an optional output directory where the processed comics will be saved, and the language for processing. The language defaults to English (`en`) if not specified.

Run the script with the following command:

```bash
python script.py --output path_to_your_output --source path_to_your_source --lang=en
```

Examples:

- Converting a folder of manga pages:

```bash
python script.py --output comic_folder --source manga_folder --lang=ja
```

- Converting a single manga page:

```bash
python script.py --output comic_folder --source manga_page.jpg --lang=en
```

This allows the script to handle different language settings for tasks like text recognition or other language-specific processing requirements.

## Contributing
Feel free to fork this repository and submit pull requests. You can also open an issue if you find any bugs or have suggestions for further enhancements.
