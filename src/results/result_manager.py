import json
import os
from datetime import datetime


class ResultManager:
    def __init__(self, folder="results"):
        self.folder = folder
        os.makedirs(folder, exist_ok=True)

    def generate_run_id(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def save_results(self, results, metadata):
        run_id = self.generate_run_id()

        data = {
            "run_id": run_id,
            "metadata": metadata,
            "results": results
        }

        file_path = os.path.join(self.folder, f"{run_id}.json")

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"\nSaved results to {file_path}")

        return file_path

    def load_results(self, file_path):
        with open(file_path, "r") as f:
            return json.load(f)