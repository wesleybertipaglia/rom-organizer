# Rom Organizer

A command-line utility for batch processing rom files for your favorite emulators. This tool provides functionalities such as renaming, compressing, converting, and resizing files and images.

## Features

- **Renamer**: Automatically rename files based on the rom signature.

- **Cleaner**: Remove duplicate files and unnecessary metadata.

- **Compressor**: Compress files to zip, 7z, rar or CHD formats.

- **ArtBox**: Copy the necessary box art images for your roms from a curated local database.

- **Auto Run**: Automatically run the pipeline of tools to process your roms in one go.

## Installation

Make sure Python 3.x is installed:

### Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate
```

### Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script to start the interactive tool menu:

```bash
python main.py
```

Follow the on-screen prompts to choose tool types and execute commands.

## Contributing

Feel free to add new tools or improve existing ones by extending the `Tool` base class and registering your commands.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
