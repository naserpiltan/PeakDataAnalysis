import ijson
import pandas as pd


class JsonManager:
    def __init__(self, json_folder_path: str):
        self.__json_foler_path = json_folder_path
