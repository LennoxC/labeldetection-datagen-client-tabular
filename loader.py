import os
from abc import ABC, abstractmethod

import PIL
import requests
from pdf2image import convert_from_bytes
from PIL import Image
import time

class Loader:
    def __init__(self, dataset_name, datasets_dir, max_per_hour=0):
        self.dataset_name = dataset_name
        self.datasets_dir = datasets_dir

        self.dataset_home = os.path.join(self.datasets_dir, dataset_name)
        self.output_folder = os.path.join(str(self.dataset_home), 'output')

        self.output_jsonl = os.path.join(str(self.output_folder), 'output.jsonl')

        self.dataset_data_home = os.path.join(str(self.dataset_home), 'data')

        self.images_dir = os.path.join(str(self.dataset_data_home), 'images')
        self.tabular_dir = os.path.join(str(self.dataset_data_home), 'tabular')

        self.count = 0

        self.max = 0

        self.max_per_hour = max_per_hour # for rate limiting. Default is 0.

        self.wait_interval = (60*60) / self.max_per_hour

        os.makedirs(self.output_folder, exist_ok=True)

    @abstractmethod
    def load_next(self):
        pass

    @abstractmethod
    def write_next(self, index, image, qas):
        pass

    def set_limit(self, limit):
        self.max = limit

    def start(self):
        print(f"{self.dataset_name} loader starting")

        while self.count < self.max or self.max == 0:
            try:
                index, image, qas = self.load_next()
                self.write_next(index, image, qas)
                self.count += 1
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"Received 429 Too Many Requests. Retrying in 10 seconds...")
                    time.sleep(10)
            except Exception as e:
                self.count += 1
                print(f"Exception: + {str(e)}")

            if self.count % 10 == 0:
                print(f"{self.count} images processed")

        print(f"{self.dataset_name} loader completed")


    def web_pdf_to_image(self, url, output_path, dpi=200):

        if self.wait_interval != 0:
            time.sleep(self.wait_interval)

        if not os.path.exists(output_path):

            headers = None
            if self.dataset_name == "supplements":

                headers = {
                    'X-Api-Key': os.getenv("NHI_API_KEY")
                }

            if headers is not None:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise error for bad status

                # Convert PDF bytes to image(s)
                images = convert_from_bytes(response.content, dpi=dpi)

                return images[0]

            elif self.dataset_name == "supplements":
                exit("api key is required for supplements api")

            else:
                response = requests.get(url)
                response.raise_for_status()  # Raise error for bad status

                # Convert PDF bytes to image(s)
                images = convert_from_bytes(response.content, dpi=dpi)

                return images[0]

        else:
            return PIL.Image.open(output_path)

    def float_to_string(self, input_num):
        return ('%.15f' % input_num).rstrip('0').rstrip('.')