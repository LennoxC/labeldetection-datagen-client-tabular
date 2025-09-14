import argparse
import os

from applications.supplements import SupplementsLoader
from applications.supplements_cleaner import SupplementsCleaner

parser = argparse.ArgumentParser(description="A script for scraping label images from the web, then creating prompts and answers from tabular data")

parser.add_argument("-app", "--application", type=str, help="The application you are targeting")
parser.add_argument("-l", "--limit", type=int, help="The dataset size limit")


args = parser.parse_args()

loader = None
datasets_home = os.environ.get('DATASOURCE_HOME')
outputs_home = os.environ.get('OUTPUTS_HOME')

if datasets_home is None or outputs_home is None:
    raise ValueError("You must set environment variable DATASOURCE_HOME and OUTPUTS_HOME")

if args.application == "supplements":
    loader = SupplementsLoader(datasets_home)
    loader.set_limit(args.limit)
if args.application == "supplements_cleaner":
    cleaner = SupplementsCleaner(outputs_home)
    cleaner.start()
else:
    print("No application specified")
    exit(0)

loader.start()


