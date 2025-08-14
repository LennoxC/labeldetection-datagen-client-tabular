import argparse
import os

from applications.supplements import SupplementsLoader

parser = argparse.ArgumentParser(description="A script for scraping label images from the web, then creating prompts and answers from tabular data")

parser.add_argument("-app", "--application", type=str, help="The application you are targeting")

args = parser.parse_args()

loader = None
datasets_home = os.environ.get('DATASOURCE_HOME')

if args.application == "supplements":
    loader = SupplementsLoader(datasets_home)
    loader.set_limit(20)
else:
    print("No application specified")
    exit(0)

loader.start()


