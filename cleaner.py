# re-iterate over the output.jsonl file to clean up the data
import json
import os

class Cleaner:
    def __init__(self, filepath, source_file_name="output.jsonl", output_file_name="output_cleaned.jsonl"):
        self.filepath = filepath

        self.datasource = os.path.join(filepath, source_file_name)
        self.output_file = os.path.join(filepath, output_file_name)

        self.data_source = []

    def start(self):
        with open(self.datasource, mode="r") as f:
            for line in f:
                obj = json.loads(line.strip())
                obj_clean = self.clean(obj)
                self.write(obj_clean)

    def write(self, obj):
        with open(self.output_file, mode="a") as f:
            json_string = json.dumps(obj)
            f.write(json_string + "\n")

    # this should be implemented in an inherited class
    def clean(self, obj):
        return obj