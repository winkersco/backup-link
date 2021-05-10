# Backup link

Backup link is a Python script for generating backup links from urls.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip3 install -r requirements.txt
```

## Usage

```
usage: backup_link.py [-h] [-e EXTENSIONS [EXTENSIONS ...]] [-s] -f INPUT_FILEPATH
                      [-o OUTPUT_FILEPATH] [-q]

Backup Link

optional arguments:
  -h, --help            show this help message and exit
  -e EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]
                        extensions that should supported in output. default=["zip",
                        "tar", "tar.gz", "rar", "sql", "gzip", "7z", "gz", "bz2"]
  -s, --shuffle         shuffle output results. default=False
  -f INPUT_FILEPATH, --file INPUT_FILEPATH
                        file containing urls, 1 host per line.
  -o OUTPUT_FILEPATH, --output OUTPUT_FILEPATH
                        file to save results. default="output.txt"
  -q, --quiet           not print status messages to stdout. Default=True
```

## Example
```bash
python3 backup_link.py -e zip rar -f input.txt -o output.txt -s
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU](https://choosealicense.com/licenses/gpl-3.0/)