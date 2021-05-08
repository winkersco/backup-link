# Backup link

Backup link is a Python script for generating backup links from urls.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
usage: backup_link.py [-h] -f INPUT_FILEPATH [-o OUTPUT_FILEPATH] [-q]

Backup Link

optional arguments:
  -h, --help            show this help message and exit
  -f INPUT_FILEPATH, --file INPUT_FILEPATH
                        File containing urls, 1 host per line.
  -o OUTPUT_FILEPATH, --output OUTPUT_FILEPATH
                        File to save results.
  -q, --quiet           Don't print status messages to stdout

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU](https://choosealicense.com/licenses/gpl-3.0/)