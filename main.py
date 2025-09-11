import argparse
import os

from applications.supplements import SupplementsLoader

parser = argparse.ArgumentParser(description="A script for scraping label images from the web, then creating prompts and answers from tabular data")

parser.add_argument("-app", "--application", type=str, help="The application you are targeting")
parser.add_argument("-l", "--limit", type=int, help="The dataset size limit")

args = parser.parse_args()

loader = None
datasets_home = os.environ.get('DATASOURCE_HOME')

if args.application == "supplements":
    loader = SupplementsLoader(datasets_home)
    loader.set_limit(args.limit)
else:
    print("No application specified")
    exit(0)

loader.start()


