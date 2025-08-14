import os
from abc import ABC, abstractmethod

import PIL
import requests
import io
from pdf2image import convert_from_bytes
from PIL import Image

class Loader:
    def __init__(self, dataset_name, datasets_dir):
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
            index, image, qas = self.load_next()
            self.write_next(index, image, qas)
            self.count += 1

            if self.count % 10 == 0:
                print(f"{self.count} images processed")

        print(f"{self.dataset_name} loader completed")


    def web_pdf_to_image(self, url, output_path, dpi=200):
        if not os.path.exists(output_path):
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad status

            # Convert PDF bytes to image(s)
            images = convert_from_bytes(response.content, dpi=dpi)

            return images[0]
        else:
            return PIL.Image.open(output_path)