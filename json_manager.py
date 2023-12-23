import ijson
import pandas as pd
import glob
import pathlib
import os

# time set is not required


class JsonManager:
    def __init__(self, json_folder_path: str):
        self.__json_folder_path = json_folder_path
        self.__json_postfix = ".json"
        self.__json_files_list =[]
        self.__get_json_files_list()
        self.read_json_files()

    def __get_json_files_list(self):
        for file in os.listdir(self.__json_folder_path):
            if file.endswith(self.__json_postfix):
                file_path = os.path.join(self.__json_folder_path, file)
                self.__json_files_list.append(file_path)

    def read_json_files(self):
        for file_path in self.__json_files_list:
            print("file path ",file_path)
            with open(file_path, 'rb') as file:
                objects = ijson.items(file, '')
                for obj in objects:
                    date_ranges = obj.get('dateRanges')
                    exclusions = obj.get('exclusions')
                    time_sets = obj.get('timeSets')
                    network = obj.get('network', {})
                    segment_results = network.get('segmentResults', [])

                    # day,month,am_pm and timerange are fixed for each segment

                    date_range = None
                    day = None
                    am_pm = None
                    month = None
                    for dr in date_ranges:
                        date_from = dr['from']
                        date_to = dr['to']
                        day = str(str(dr['name']).split(" ")[0]).split("-")[0]
                        am_pm = str(str(dr['name']).split(" ")[0]).split("-")[1]
                        month = str(str(dr['name']).split(" ")[0]).split("-")[2]
                        year = str(dr['name']).split(" ")[1]
                        date_range = date_from+" to "+date_to

                    for segment in segment_results:
                        segment_id = segment['segmentId']
                        frc = segment.get('frc')

                        #address
                        street_name = segment.get('streetName')
                        distance = segment.get('distance')
                        speed_limit = segment.get('speedLimit')

                        shape = segment.get('shape')
                        start_lat = shape[0]['latitude']
                        start_long = shape[0]['longitude']
                        end_lat = shape[-1]['latitude']
                        end_long = shape[-1]['longitude']

                        print("day ", day, " am_pm ", am_pm, " month ", month, " segment_id ", segment_id, " frc ", frc)
                        print("start_lat ", start_lat, " start_long ", start_long, " end_lat ", end_lat, " end_long ", end_long)










