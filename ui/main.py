import ijson
import numpy
import argparse
from pathlib import Path
from json_manager import JsonManager
def main(json_folder_apth):

    json_manager = JsonManager(json_folder_apth)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--json_folder_path")

    args = parser.parse_args()

    json_folder_path = Path(args.json_folder_path)

    main(json_folder_path)

