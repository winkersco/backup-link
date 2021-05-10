import argparse
import os
import random
import re
import sys
import time

from progressbar import progressbar


class BackupLink:
    """MikrotikExtractor class object"""

    def __init__(self, extensions, shuffle, input_filepath, output_filepath, verbose):
        """Initialize MikrotikExtractor class object."""

        self.extensions = extensions
        self.shuffle = shuffle
        with open(input_filepath) as self.input_file:
            self.urls = self.input_file.read().splitlines()
        self.output_filepath = output_filepath
        self.verbose = verbose
        self.backups = []

    def append_output(self, backups):
        """Create output for links"""
        with open(self.output_filepath, 'a') as file:
            file.writelines('\n'.join(backups) + '\n')

    def create_shuffle_output(self):
        random.shuffle(self.backups)
        with open('shuffle-' + self.output_filepath, 'a') as file:
            file.writelines('\n'.join(self.backups))

    def run(self):
        """Run backup link"""

        if not self.verbose:
            self.urls = progressbar(self.urls)

        for i, url in enumerate(self.urls):
            m = re.search(
                '(?P<protocol>https?://)?(?P<domain>[A-Za-z_0-9-]+\.)(?P<top_level_domain>([A-Za-z]+\.)?[A-Za-z]+).*',
                url)
            if m:
                protocol = m.group('protocol') if m.group('protocol') else ''
                domain = m.group('domain')
                top_level_domain = m.group('top_level_domain')

                if self.verbose:
                    print(f'[+] Processing {url} ({i + 1}/{len(self.urls)})')

                for extension in self.extensions:
                    backups = [
                        f'{protocol}{domain}{top_level_domain}/{domain}{extension}',
                        f'{protocol}{domain}{top_level_domain}/{domain}{top_level_domain}.{extension}',
                        f'{protocol}{domain}{top_level_domain}/www.{domain}{extension}',
                        f'{protocol}{domain}{top_level_domain}/www.{domain}{top_level_domain}.{extension}',
                    ]

                    self.append_output(backups)
                    self.backups = self.backups + backups

        if self.shuffle:
            self.create_shuffle_output()


def get_timestamp():
    """Retrieve a pre-formatted datetime."""

    now = time.localtime()
    timestamp = time.strftime('%Y%m%d_%H%M%S', now)
    return timestamp


def run():
    """Run entrypoint."""

    parser = argparse.ArgumentParser(description='Backup Link')
    parser.add_argument(
        '-e', '--extensions', dest='extensions', action='store', nargs='+',
        default=['zip', 'tar', 'tar.gz', 'rar', 'sql', 'gzip', '7z', 'gz', 'bz2'],
        help='extensions that should supported in output. '
             'default=["zip", "tar", "tar.gz", "rar", "sql", "gzip", "7z", "gz", "bz2"]'
    )
    parser.add_argument(
        '-s', '--shuffle', dest='shuffle', action="store_true", required=False, default=False,
        help='shuffle output results. default=False',
    )
    parser.add_argument(
        '-f', '--file', dest='input_filepath', action='store', required=True,
        help='file containing urls, 1 host per line.'
    )
    parser.add_argument(
        '-o', '--output', dest='output_filepath', action='store', default='output.txt',
        help='file to save results. default="output.txt"'
    )
    parser.add_argument('-q', '--quiet', action='store_false', dest='verbose', default=True,
                        help='not print status messages to stdout. Default=True')

    args = parser.parse_args()

    if args.verbose:
        print(f'[+] Initiation timestamp: {get_timestamp()}')

    if not os.path.exists(args.input_filepath):
        print('[-] Specify a valid filepath containing urls with -f')
        sys.exit(0)

    if os.path.exists(args.output_filepath):
        print(f'[*] File [{args.output_filepath}] has already exists. urls will write in append mode.')

    if args.shuffle and os.path.exists('shuffle-' + args.output_filepath):
        print(f'[*] File [shuffle-{args.output_filepath}] has already exists. urls will write in append mode.')

    mikrotik_extractor = BackupLink(**vars(args))
    mikrotik_extractor.run()

    if args.verbose:
        print(f'[+] Completion timestamp: {get_timestamp()}')
        print('[+] Done')


if __name__ == '__main__':
    run()
