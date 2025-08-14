import numpy as np
import pandas as pd
from loader import Loader
import os
import json
import random
import re

class SupplementsLoader(Loader):
    def __init__(self, datasets_home):
        super(SupplementsLoader, self).__init__("supplements", datasets_home)

        self.processed_max = 0

        self.products_csv = os.path.join(self.tabular_dir, "products.csv")
        self.supplements_csv = os.path.join(self.tabular_dir, "supplementfacts.csv")

        self.products_df = pd.read_csv(self.products_csv)
        self.supplements_df = pd.read_csv(self.supplements_csv)
        self.dataset_columns = ["id", "label_image_url", "product_name", "brand_name", "barcode_number", "net_contents", "serving_size", "suggested_use", "other_ingredients", "company_name"]
        self.sample_columns = ["product_name", "brand_name", "net_contents", "serving_size", "company_name"]

    def load_next(self):
        next_index = self.processed_max + 1
        product = self.products_df.iloc[next_index]

        product_id = product["id"]
        label_image_url = product["label_image_url"]

        image = self.web_pdf_to_image(label_image_url, self.get_image_file(next_index))

        qas = self.create_prompts_answers(product)

        self.processed_max += 1

        return next_index, image, qas

    def write_next(self, index, image, qas):
        image_output_file = self.get_image_file(index)

        output_text_object = {
            "image": image_output_file,
            "qas": qas
        }

        try:
            json_line = json.dumps(output_text_object)
            with open(self.output_jsonl, "a") as f:
                f.write(json_line + '\n')
            image.save(image_output_file)
        except Exception as e:
            print("Error writing files: " + str(e))

    def get_image_file(self, index):
        return os.path.join(str(self.images_dir), str(index) + ".jpg")

    def create_prompts_answers(self, label):
        pairs = []

        for propery in self.sample_columns:
            answer = label[propery]
            if answer is not None:
                q, a = self.process_column(propery, answer)
                pairs.append({"q": q, "a": a})

        return pairs

    def process_column(self, column_name, value):
        #["product_name", "brand_name", "net_contents", "serving_size", "company_name"]

        if column_name == "product_name":
            return "What is the name of the product?", value
        if column_name == "brand_name":
            return "What is the name of the brand?", value
        if column_name == "net_contents":
            return "What is the numeric component of the product contents?", re.findall(r"\d+", value)[0]
        if column_name == "serving_size":
            return "What is the numeric component of the product serving size?", re.findall(r"\d+", value)[0]
        if column_name == "company_name":
            return "What is the name of the company who produced this product?", value
        else:
            return "", ""

