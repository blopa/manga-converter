# Manga to Comics Converter

This Python script converts manga pages into Western comic-style pages by reversing the reading direction, among other transformations.

## Installation

First, clone the repository or download the files to your local machine.

Before running the script, you need to install the required Python libraries. Run the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Usage
To use the script, you need to specify the source directory (or file) containing the manga images and an optional output directory where the processed comics will be saved. If the output directory is not specified, the script will create a default output directory in the same location as the source.

Run the script with the following command:

```bash
python3 script.py --source path_to_your_source --output path_to_your_output
```

Examples:

- Converting a folder of manga pages:

```bash
python3 script.py --source manga_folder --output comic_folder
```

- Converting a single manga page:

```bash
python3 script.py --source manga_page.jpg --output comic_folder
```

The above command will process page1.png and place the converted comic page in the same directory as the source file.

## Contributing
Feel free to fork this repository and submit pull requests. You can also open an issue if you find any bugs or have suggestions for further enhancements.
