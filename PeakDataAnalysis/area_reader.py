import pandas as pd
import openpyxl
import xlsxwriter

import os

class AreaReader:
    def __init__(self, area_file_path: str):
        self.area_file_path = area_file_path
        self._area_dict = {}
        self.__local_board_dict = {}
        self.__init_local_board_dict()
        self.__get_area_dict()
    def __get_area_dict(self):
        if not os.path.exists(self.area_file_path):
            print("Excel file path doesnt exist: ", self.area_file_path)
            return

        sheet_name = 0
        df = pd.read_excel(self.area_file_path, sheet_name=sheet_name)

        # Convert the DataFrame to a dictionary with column headers as keys
        # and lists of row entries as values
        #self._area_dict = df.to_dict(orient='list')
        for index, row in df.iterrows():
            key = row.iloc[0]  # First column value is the key
            values = row.iloc[1:].tolist()  # Other columns values as a list
            direction = self.__local_board_dict[values[1]]
            self._area_dict[key] = values

    def get_localBaord_area_direction(self, link_id):
        local_board_area = self._area_dict[link_id]
        local_board = local_board_area[1]
        area = local_board_area[2]
        direction = self.__local_board_dict[local_board]
        return local_board, area, direction

    def __init_local_board_dict(self):
        self.__local_board_dict = {
            "Rodney": "North",
            "Hibiscus and Bays": "North",
            "Upper Harbour": "North",
            "Kaipatiki": "North",
            "Devonport-Takapuna": "North",
            "Henderson-Massey": "West",
            "Waitakere Ranges": "West",
            "Maungakiekie-Tamaki": "East",
            "Howick": "East",
            "Mangere-Otahuhu": "South",
            "Otara-Papatoetoe": "South",
            "Manurewa": "South",
            "Papakura": "South",
            "Franklin": "South",
            "Waitemata": "Center",
            "Whau": "Center",
            "Albert-Eden": "Center",
            "Puketapapa": "Center",
            "Orakei": "Center"
        }



