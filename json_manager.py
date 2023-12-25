import ijson
import pandas as pd
import glob
import pathlib
import os
from holidays_manager import HolidaysManager
from date_time_manager import DateTimeManager
from excel_exporter import ExcelExporter

# time set is not required

class JsonManager:
    def __init__(self, json_folder_path: str):
        self.__json_folder_path = json_folder_path
        self.__json_postfix = ".json"
        self.__json_files_list = []
        self.__export_columns_list = []
        self.__export_columns_dict = {}
        self.__init_export_columns()
        self.__init_export_columns_dict()

        self.__holidays_manager = HolidaysManager()
        self.__date_time_manager = DateTimeManager()

        excel_directory_path = str(json_folder_path)
        excel_directory_path = excel_directory_path.replace("\\","/")
        excel_directory_path = excel_directory_path.replace("\\","/")

        parts = excel_directory_path.split("/")
        last_slash_loc = excel_directory_path.rfind("/")
        excel_directory_path = excel_directory_path[:last_slash_loc]
        excel_directory_path = excel_directory_path + "/excel"
        self.__excel_exporter = ExcelExporter(excel_directory_path)

        self.__get_json_files_list()
        self.read_json_files()





    def __get_json_files_list(self):
        for file in os.listdir(self.__json_folder_path):
            if file.endswith(self.__json_postfix):
                file_path = os.path.join(self.__json_folder_path, file)
                self.__json_files_list.append(file_path)

    def read_json_files(self):
        for file_path in self.__json_files_list:
            print("file path ", file_path)
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
                    is_public_holidays = None
                    is_school_holidays = None
                    is_day_after_public_holiday = None
                    is_day_before_public_holiday = None
                    is_weekend = None
                    is_weekday = None

                    for dr in date_ranges:
                        date_from = dr['from']
                        date_from_pd = pd.to_datetime(date_from)
                        date_to = dr['to']
                        day = str(str(dr['name']).split(" ")[0]).split("-")[0]
                        #there are some typos in the name o
                        day = self.__date_time_manager.refine_day_name(day)
                        am_pm = str(str(dr['name']).split(" ")[0]).split("-")[1]
                        month = str(str(dr['name']).split(" ")[0]).split("-")[2]
                        year = str(dr['name']).split(" ")[1]
                        date_range = date_from + " to " + date_to
                        is_public_holidays = self.__holidays_manager.is_public_holiday(year, month, day)
                        is_school_holidays = self.__holidays_manager.is_school_holiday(year, month, day)
                        is_day_after_public_holiday = self.__holidays_manager.is_day_after_holiday(year, month, day)
                        is_day_before_public_holiday = self.__holidays_manager.is_day_before_holiday(year, month, day)
                        is_weekend = self.__holidays_manager.is_weekend(day)
                        is_weekday = not is_weekend

                    print("day:", day, " month:", month, " year:", year, " ph:", is_public_holidays, " dbph:",
                          is_day_before_public_holiday,
                          " daph:", is_day_after_public_holiday, " isschool:", is_school_holidays, " weekend:",
                          is_weekend, " weekday:", is_weekday)

                    for segment in segment_results:
                        segment_id = segment['segmentId']
                        frc = segment.get('frc')

                        # address
                        street_name = segment.get('streetName')
                        distance = segment.get('distance')
                        speed_limit = segment.get('speedLimit')

                        shape = segment.get('shape')
                        start_lat = shape[0]['latitude']
                        start_long = shape[0]['longitude']
                        end_lat = shape[-1]['latitude']
                        end_long = shape[-1]['longitude']

                        segment_time_results = segment.get('segmentTimeResults')
                        for segment_time in segment_time_results:
                            speed_percentiles_list = segment_time['speedPercentiles']


                        # print("start_lat ", start_lat, " start_long ", start_long, " end_lat ", end_lat, " end_long ",
                        #      end_long)
                        self.__append_to_export_columns_dict(segment_id, day, month, date_range, street_name, start_lat,
                                                             start_long, end_lat, end_long, distance, speed_limit,
                                                             is_public_holidays, is_day_before_public_holiday,
                                                             is_day_after_public_holiday, is_school_holidays,
                                                             is_weekend, is_weekday, frc, speed_percentiles_list)
        self.__excel_exporter.write(self.__export_columns_dict)


    def __init_export_columns_dict(self):

        for column in self.__export_columns:
            self.__export_columns_dict[column] = []

    def __init_export_columns(self):
        self.__export_columns = ['segment_id', 'day', 'Month', 'Date', 'Address', 'Start_lat', 'Start_long',
                                 'End_lat', 'End_long', 'Distance', 'Speed_limit', 'Public_holidays',
                                 'Day_before_public_holidays', 'Day_after_public_holidays', 'School_holidays',
                                 'Weekend', 'Weekday', 'Frc']

    def __append_to_export_columns_dict(self, segment_id, day, month, date, address, start_lat, star_long,
                                        end_lat, end_long, distance, speed_limit, public_holidays,
                                        day_before_public_holidays, day_after_public_holidays,
                                        school_holidays, weekend, weekday, frc, speed_percentiles_list
                                        ):

        self.__export_columns_dict[self.__export_columns[0]].append(segment_id)
        self.__export_columns_dict[self.__export_columns[1]].append(day)
        self.__export_columns_dict[self.__export_columns[2]].append(month)
        self.__export_columns_dict[self.__export_columns[3]].append(date)
        self.__export_columns_dict[self.__export_columns[4]].append(address)
        self.__export_columns_dict[self.__export_columns[5]].append(start_lat)
        self.__export_columns_dict[self.__export_columns[5]].append(star_long)
        self.__export_columns_dict[self.__export_columns[6]].append(end_lat)
        self.__export_columns_dict[self.__export_columns[7]].append(end_long)
        self.__export_columns_dict[self.__export_columns[8]].append(distance)
        self.__export_columns_dict[self.__export_columns[9]].append(speed_limit)
        self.__export_columns_dict[self.__export_columns[10]].append(public_holidays)
        self.__export_columns_dict[self.__export_columns[11]].append(day_before_public_holidays)
        self.__export_columns_dict[self.__export_columns[12]].append(day_after_public_holidays)
        self.__export_columns_dict[self.__export_columns[13]].append(school_holidays)
        self.__export_columns_dict[self.__export_columns[14]].append(weekend)
        self.__export_columns_dict[self.__export_columns[15]].append(weekday)
        self.__export_columns_dict[self.__export_columns[16]].append(frc)

        # for index , speed_percent in enumerate(speed_percentiles_list):
        #     self.__export_columns_dict[self.__export_columns[17+index]].append(speed_percentiles_list[index])




