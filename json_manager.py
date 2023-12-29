import ijson
import pandas as pd
import glob
import pathlib
import os
from holidays_manager import HolidaysManager
from date_time_manager import DateTimeManager
from excel_exporter import ExcelExporter
from peak_hour_extractor import PeakHourExtractor, TimeType

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
        for file_index, file_path in enumerate(self.__json_files_list):
            print("file path ", file_path, " : ", file_index+1, " / ", len(self.__json_files_list))
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

                    # print("day:", day, " month:", month, " year:", year, " ph:", is_public_holidays, " dbph:",
                    #       is_day_before_public_holiday,
                    #       " daph:", is_day_after_public_holiday, " isschool:", is_school_holidays, " weekend:",
                    #       is_weekend, " weekday:", is_weekday)

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
                        time_type = TimeType.AM
                        if am_pm == "PM":
                            time_type = TimeType.PM

                        peak_hour_finder = PeakHourExtractor(segment_time_results, time_type)
                        peak_hour = peak_hour_finder.calculate_peak_hour()
                        peak_period_1_hour_a = peak_hour_finder.get_peak_period_1_hour_a()
                        peak_period_2_hour_a = peak_hour_finder.get_peak_period_2_hour_a()
                        peak_period_1_hour_b = peak_hour_finder.get_peak_period_1_hour_b()

                        is_percentile_reliable = peak_hour_finder.is_percentile_reliable()
                        is_sample_size_reliable = peak_hour_finder.is_sample_size_reliable()

                        self.__append_to_export_columns_dict(segment_id, day, month, date_range, street_name, start_lat,
                                                             start_long, end_lat, end_long, distance, speed_limit,
                                                             is_public_holidays, is_day_before_public_holiday,
                                                             is_day_after_public_holiday, is_school_holidays,
                                                             is_weekend, is_weekday, frc, peak_hour, peak_period_1_hour_a,
                                                             peak_period_2_hour_a, peak_period_1_hour_b,
                                                             is_sample_size_reliable, is_percentile_reliable)
        self.__excel_exporter.write(self.__export_columns_dict)


    def __init_export_columns_dict(self):

        for column in self.__export_columns:
            self.__export_columns_dict[column] = []

    def __init_export_columns(self):
        self.__export_columns = ['segment_id', 'day', 'Month', 'Date', 'Address', 'Start_lat', 'Start_long',
                                 'End_lat', 'End_long', 'Distance', 'Speed_limit', 'Public_holidays',
                                 'Day_before_public_holidays', 'Day_after_public_holidays', 'School_holidays',
                                 'Weekend', 'Weekday', 'Frc', 'Peak_hour', 'Peak_period_1_hour_a',
                                 'Peak_period_2_hour_a', 'Peak_period_1_hour_b',
                                 'Reliability_sample_size', 'Reliability_percentile']

    def __append_to_export_columns_dict(self, segment_id, day, month, date, address, start_lat, star_long,
                                        end_lat, end_long, distance, speed_limit, public_holidays,
                                        day_before_public_holidays, day_after_public_holidays,
                                        school_holidays, weekend, weekday, frc, peak_hour, peak_period_1_hour_a,
                                        peak_period_2_hour_a, peak_period_1_hour_b,
                                        is_sample_size_reliable, is_percentile_reliable
                                        ):

        self.__export_columns_dict[self.__export_columns[0]].append(segment_id)
        self.__export_columns_dict[self.__export_columns[1]].append(day)
        self.__export_columns_dict[self.__export_columns[2]].append(month)
        self.__export_columns_dict[self.__export_columns[3]].append(date)
        self.__export_columns_dict[self.__export_columns[4]].append(address)
        self.__export_columns_dict[self.__export_columns[5]].append(start_lat)
        self.__export_columns_dict[self.__export_columns[6]].append(star_long)
        self.__export_columns_dict[self.__export_columns[7]].append(end_lat)
        self.__export_columns_dict[self.__export_columns[8]].append(end_long)
        self.__export_columns_dict[self.__export_columns[9]].append(distance)
        self.__export_columns_dict[self.__export_columns[10]].append(speed_limit)
        self.__export_columns_dict[self.__export_columns[11]].append(public_holidays)
        self.__export_columns_dict[self.__export_columns[12]].append(day_before_public_holidays)
        self.__export_columns_dict[self.__export_columns[13]].append(day_after_public_holidays)
        self.__export_columns_dict[self.__export_columns[14]].append(school_holidays)
        self.__export_columns_dict[self.__export_columns[15]].append(weekend)
        self.__export_columns_dict[self.__export_columns[16]].append(weekday)
        self.__export_columns_dict[self.__export_columns[17]].append(frc)
        self.__export_columns_dict[self.__export_columns[18]].append(peak_hour)
        self.__export_columns_dict[self.__export_columns[19]].append(peak_period_1_hour_a)
        self.__export_columns_dict[self.__export_columns[20]].append(peak_period_2_hour_a)
        self.__export_columns_dict[self.__export_columns[21]].append(peak_period_1_hour_b)
        self.__export_columns_dict[self.__export_columns[22]].append(is_sample_size_reliable)
        self.__export_columns_dict[self.__export_columns[23]].append(is_percentile_reliable)

        # for index , speed_percent in enumerate(speed_percentiles_list):
        #     self.__export_columns_dict[self.__export_columns[17+index]].append(speed_percentiles_list[index])




