import argparse
import os
import random
import re
import sys
import time


class BackupLink:
    """MikrotikExtractor class object"""

    def __init__(self, input_filepath, output_filepath, verbose):
        """Initialize MikrotikExtractor class object."""
        with open(input_filepath) as self.input_file:
            self.urls = self.input_file.read().splitlines()
        self.output_filepath = output_filepath
        self.verbose = verbose
        self.backup_links = []

    def create_output(self):
        with open(self.output_filepath, 'w') as file:
            file.writelines('\n'.join(self.backup_links))

    def run(self):
        """Run backup link"""

        for index, url in enumerate(self.urls):
            m = re.search(
                '(?P<protocol>https?://)?(?P<domain>[A-Za-z_0-9-]+\.)(?P<top_level_domain>([A-Za-z]+\.)?[A-Za-z]+).*',
                url)
            if m:
                protocol = m.group('protocol') if m.group('protocol') else ''
                # cname = m.group('cname') if m.group('cname') else ''
                domain = m.group('domain')
                top_level_domain = m.group('top_level_domain')

                print(protocol, domain, top_level_domain)

                extensions = ['zip', 'tar', 'tar.gz', 'rar', 'sql', 'gzip', '7z', 'gz', 'bz2']
                for extension in extensions:
                    backups = [
                        f'{protocol}{domain}{top_level_domain}/{domain}{extension}',
                        f'{protocol}{domain}{top_level_domain}/{domain}{top_level_domain}.{extension}',
                        f'{protocol}{domain}{top_level_domain}/www.{domain}{extension}',
                        f'{protocol}{domain}{top_level_domain}/www.{domain}{top_level_domain}.{extension}',
                    ]
                    for backup in backups:
                        self.backup_links.append(backup)

                random.shuffle(self.backup_links)

                for backup in self.backup_links:
                    if self.verbose:
                        print(backup)

        if self.output_filepath:
            self.create_output()


def get_timestamp():
    """Retrieve a pre-formatted datetime."""

    now = time.localtime()
    timestamp = time.strftime("%Y%m%d_%H%M%S", now)
    return timestamp


def run():
    """Run entrypoint."""

    parser = argparse.ArgumentParser(description="Backup Link")
    parser.add_argument(
        "-f", "--file", dest="input_filepath", action="store", required=True,
        help="File containing urls, 1 host per line."
    )
    parser.add_argument(
        "-o", "--output", dest="output_filepath", action="store", help="File to save results."
    )
    parser.add_argument("-q", "--quiet", action="store_false", dest="verbose", default=True,
                        help="Don't print status messages to stdout")

    args = parser.parse_args()

    if not os.path.exists(args.input_filepath):
        print("[-] Specify a valid filepath containing urls with -f")
        sys.exit(0)

    if args.verbose:
        print(f"[*] Initiation timestamp: {get_timestamp()}")

    mikrotik_extractor = BackupLink(**vars(args))
    mikrotik_extractor.run()

    if args.verbose:
        print(f"[*] Completion timestamp: {get_timestamp()}")
        print('[*] Done')


if __name__ == '__main__':
    run()
