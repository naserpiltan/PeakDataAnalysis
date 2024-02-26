import ijson
import numpy
import argparse
from pathlib import Path
from json_manager import JsonManager


def main(json_folder_path, links_folder_path, area_local_board_file_path):

    json_manager = JsonManager(json_folder_path, links_folder_path, area_local_board_file_path)
    json_manager.read_json_files()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--json_folder_path")

    parser.add_argument("--links_folder_path")

    parser.add_argument("--area_local_board_file_path")

    args = parser.parse_args()

    json_folder_path = Path(args.json_folder_path)

    links_folder_path = Path(args.links_folder_path)

    area_local_board_file_path = Path(args.area_local_board_file_path)

    main(json_folder_path, links_folder_path, area_local_board_file_path)

