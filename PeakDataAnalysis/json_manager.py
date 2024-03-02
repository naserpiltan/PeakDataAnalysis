import ijson
import pandas as pd
import glob
import pathlib
import os
from holidays_manager import HolidaysManager
from date_time_manager import DateTimeManager
from excel_exporter import ExcelExporter
from peak_hour_extractor import PeakHourExtractor, TimeType
from area_reader import AreaReader
from PyQt6 import QtCore
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty, QStringListModel, QVariant, QAbstractListModel, \
    Qt, QUrl
from link_files_reader import LinkFileReader
import re
import time

import sqlite3
import json
from decimal import Decimal
from datetime import datetime, timedelta

from DBConnection import DatabaseWrapper

class JsonManager(QObject):
    progress_value_changed = QtCore.pyqtSignal(int)

    def __init__(self, json_folder_path: str, links_folder_path: str, area_file_path,  parent=None):
        super().__init__(parent)

        # whenever one json file gets processed, this signal will be emitted
        self.__jsons_root_folder_path = json_folder_path
        self.__json_postfix = ".json"
        self.__day_json_files_dict = {}
        self.__export_columns_list = []
        self.__export_columns_dict = {}

        self.__area_reader = AreaReader(area_file_path)
        self.__links_file_reader = LinkFileReader(links_folder_path)
        self.__links_segments_list = {}

        self.__links_segments_ids_dict = {}

        self.__database_wrapper = DatabaseWrapper(self.__jsons_root_folder_path)

        self.__init_export_columns()
        self.__init_export_columns_dict()

        self.__holidays_manager = HolidaysManager()
        self.__date_time_manager = DateTimeManager()

        excel_directory_path = str(json_folder_path)
        excel_directory_path = excel_directory_path.replace("\\", "/")
        excel_directory_path = excel_directory_path.replace("\\", "/")

        parts = excel_directory_path.split("/")
        last_slash_loc = excel_directory_path.rfind("/")
        excel_directory_path = excel_directory_path[:last_slash_loc]
        excel_directory_path = excel_directory_path + "/excel"
        self.__excel_exporter = ExcelExporter(excel_directory_path)

        self.__days_indexes = None  # number of days
        self.__months_indexes = None  # number of months
        self.__day_time_indexes = None  # am-pm
        self.__public_holidays_indexes = None  # number of public holidays
        self.__school_holidays_indexes = None
        self.__frc_indexes = None

        self.__speed_percentile_time_sets_indexes_am = None
        self.__speed_percentile_time_sets_indexes_pm = None
        self.__sample_size_time_sets_indexes_am = None
        self.__sample_size_time_sets_indexes_pm = None

        self.__classification_index = 0
        self.__sample_size_threshold = 0
        self.__speed_percentile_diff_thresh = 0
        self.__sample_size_check_Index = 0
        self.__day_time_types = ["AM", "PM"]

        self.__get_json_files_list()

    def set_lists(self,
                  days_indexes,
                  months_indexes,
                  day_time_indexes,
                  public_h_indexes,
                  school_h_indexes,
                  frc_indexes,
                  s_p_time_set_indexes_am,
                  s_p_time_set_indexes_pm,
                  s_p_diff_threshold,
                  s_s_time_set_indexes_am,
                  s_s_time_set_indexes_pm,
                  s_s_check_index,
                  classification_index,
                  sample_size):

        self.__days_indexes = days_indexes
        self.__months_indexes = months_indexes
        self.__day_time_indexes = day_time_indexes
        self.__public_holidays_indexes = public_h_indexes
        self.__school_holidays_indexes = school_h_indexes
        self.__frc_indexes = frc_indexes

        self.__speed_percentile_time_sets_indexes_am = s_p_time_set_indexes_am
        self.__speed_percentile_time_sets_indexes_pm = s_p_time_set_indexes_pm
        self.__sample_size_time_sets_indexes_am = s_s_time_set_indexes_am
        self.__sample_size_time_sets_indexes_pm = s_s_time_set_indexes_pm
        self.__speed_percentile_diff_thresh = s_p_diff_threshold

        self.__classification_index = classification_index
        self.__sample_size_threshold = sample_size
        self.__sample_size_check_Index = s_s_check_index
        self.__excel_exporter.set_similarity_criteria_index(self.__classification_index)
        self.__holidays_manager.set_holidays_indexes(public_h_indexes,
                                                     school_h_indexes)
        print("Lists are set")

    def __is_day_name_included(self, day_name):
        for day_index, state in enumerate(self.__days_indexes):
            if not state:
                continue

            included_day_name = self.__date_time_manager.get_day_name(day_index)
            if day_name == included_day_name:
                return True
        return False

    def __is_month_name_included(self, month_name):
        for day_index, state in enumerate(self.__months_indexes):
            if not state:
                continue

            included_day_name = self.__date_time_manager.get_month_name(day_index)
            if month_name == included_day_name:
                return True
        return False

    def __is_day_time_included(self, day_time):
        for day_time_index, state in enumerate(self.__day_time_indexes):
            if not state:
                continue

            if day_time == self.__day_time_types[day_time_index]:
                return True

        return False

    def __is_frc_included(self, frc):
        for frc_index, state in enumerate(self.__frc_indexes):
            if not state:
                continue

            if frc == frc_index:
                return True

        return False

    def __is_speed_percentile_included(self, segment_time_results, time_type):

        # 20 time sets
        time_sets_indexes = []
        if time_type == TimeType.AM:
            time_sets_indexes = self.__speed_percentile_time_sets_indexes_am
        else:
            time_sets_indexes = self.__speed_percentile_time_sets_indexes_pm

        # if none of the items is True, it means all the time sets are excluded
        if not any(time_sets_indexes):
            return False

        result = True
        for s_p_index, state in enumerate(time_sets_indexes):
            if not state:
                continue

            percentile_list = segment_time_results[s_p_index]["speedPercentiles"]

            percentile_lower_bound = 0
            percentile_upper_bound = 18
            percentile_diff = abs(int(percentile_list[percentile_upper_bound]) -
                                  int(percentile_list[percentile_lower_bound]))

            if percentile_diff < self.__speed_percentile_diff_thresh:
                result = False
                break

        return result

    def __is_time_set_sample_size_included(self, segment_time_results, time_type):

        # 20 time sets
        time_sets_indexes = []
        if time_type == TimeType.AM:
            time_sets_indexes = self.__sample_size_time_sets_indexes_am
        else:
            time_sets_indexes = self.__sample_size_time_sets_indexes_pm

        # if none of the items is True, it means all the time sets are excluded
        if not any(time_sets_indexes):
            return False

        result = True
        for s_s_index, state in enumerate(time_sets_indexes):
            if not state:
                continue

            sample_size = int(segment_time_results[s_s_index]["sampleSize"])

            if sample_size < self.__sample_size_threshold:
                result = False
                break

        return result

    def __is_peak_hour_sample_size_included(self, segment_time_results, peak_hour_index):
        if peak_hour_index < 0:
            return False

        peak_hour_sample_size = segment_time_results[peak_hour_index]["sampleSize"]
        if peak_hour_sample_size < self.__sample_size_threshold:
            return False
        return True

    def __get_json_files_list(self):

        if not os.path.exists(self.__jsons_root_folder_path):
            print("Root path doesn't exist, path: ", self.__jsons_root_folder_path)
            return

        days_list = self.__date_time_manager.get_days_list()
        for day in days_list:
            day_abbr = day[:3]
            day_folder_path = os.path.join(self.__jsons_root_folder_path, day_abbr)
            if not os.path.exists(day_folder_path):
                print("Sub-folder Path doesn't exist, path ", day_folder_path)
                continue
            for file in os.listdir(day_folder_path):
                if file.endswith(self.__json_postfix):
                    file_path = os.path.join(day_folder_path, file)
                    if day_abbr not in list(self.__day_json_files_dict.keys()):
                        self.__day_json_files_dict[day_abbr] = []
                    self.__day_json_files_dict[day_abbr].append(file_path)

        # if len(str(self.__json_folder_path)) == 0:
        #     print("JSON files folder path is empty")
        #     return
        # for file in os.listdir(self.__json_folder_path):
        #     if file.endswith(self.__json_postfix):
        #         file_path = os.path.join(self.__json_folder_path, file)
        #         self.__json_files_list.append(file_path)

    def average(self, lst):
        if len(lst) == 0:
            return 0
        return sum(lst) / len(lst)

    def average_datetime(self, date_times):
        # Convert each datetime to total minutes
        total_minutes = sum(dt.hour * 60 + dt.minute for dt in date_times)

        # Calculate the average minutes
        avg_minutes = total_minutes / len(date_times)

        # Convert average minutes back to hours and minutes
        avg_hours = int(avg_minutes // 60)
        avg_minutes = int(avg_minutes % 60)

        avg_date_time = f"{avg_hours}:{avg_minutes}"
        avg_date_time = datetime.strptime(avg_date_time, "%H:%M")

        # Construct a new datetime object for the average time (date part can be arbitrary)
        #avg_datetime = datetime(2022, 1, 1, avg_hours, avg_minutes)

        return avg_date_time

    def get_seasonality_averages(self, seasonality_dict):

        # key is (link_id, day),
        # values are : peak_hour, peak_interval, peak_hour_average_travel_time,
        # peak_interval_average_travel_time, peak_hour_day_time
        for key in seasonality_dict:
            values_list = seasonality_dict[key]

            peak_hour_average_travel_times_list = []
            peak_interval_average_travel_times_list = []

            for values in values_list:
                peak_hour = values[0]
                peak_period = values[1]

                peak_hour_start = str(peak_hour).split("-")[0]
                peak_hour_start = datetime.strptime(peak_hour_start, "%H:%M")
                peak_interval_start = str(peak_period).split("-")[0]
                peak_interval_start = datetime.strptime(peak_interval_start, "%H:%M")

                peak_hour_average_travel_times_list.append(peak_hour_start)
                peak_interval_average_travel_times_list.append(peak_interval_start)

            peak_hours_average = 0
            peak_intervals_average = 0
            if not len(peak_hour_average_travel_times_list) == 0:
                peak_hours_average = self.average_datetime(peak_hour_average_travel_times_list)
                peak_intervals_average = self.average_datetime(peak_interval_average_travel_times_list)

            averages = (peak_hours_average, peak_intervals_average)
            seasonality_dict[key] = averages

        return seasonality_dict

    def get_seasonalities(self, peak_hour_average, peak_interval_average,
                          peak_hour: str, peak_interval: str):

        peak_hour_start = str(peak_hour).split("-")[0]
        peak_hour_start = datetime.strptime(peak_hour_start, "%H:%M")

        time_delta = peak_hour_start - peak_hour_average
        total_seconds = time_delta.total_seconds()
        sign = "" if total_seconds >= 0 else "-"
        # Calculate hours, minutes, and seconds
        total_seconds = abs(total_seconds)
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        peak_hour_seasonality = f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}"


        peak_interval_start = str(peak_interval).split("-")[0]
        peak_interval_start = datetime.strptime(peak_interval_start, "%H:%M")
        time_delta = peak_interval_start - peak_interval_average
        total_seconds = time_delta.total_seconds()
        sign = "" if total_seconds >= 0 else "-"
        total_seconds = abs(total_seconds)

        # Calculate hours, minutes, and seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        peak_interval_seasonality = f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}"


        # hour = str(peak_interval_start).split(":")[0]
        # minute = str(peak_interval_start).split(":")[1]
        # hour = int(hour)
        # minute = int(minute) / 60
        # digit_time = hour + minute
        # peak_interval_seasonality = float(digit_time) - float(peak_interval_average)
        return peak_hour_seasonality, peak_interval_seasonality

    def numeric_to_time(self, numeric_value):
        # Convert the numerical value to total seconds (considering positive or negative)
        total_seconds = int(numeric_value * 1440 * 60)

        # Calculate hours, minutes, and seconds (absolute value used for calculation)
        hours = abs(total_seconds) // 3600
        minutes = (abs(total_seconds) % 3600) // 60
        seconds = abs(total_seconds) % 60

        # Adjust hours to be within 0 to 23
        hours = hours % 24

        # Format the time string manually to handle negative values
        time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        if numeric_value < 0:
            time_string = "-" + time_string

        return time_string

    def get_day_time(self, peak_hour):
        am_thresh = datetime.strptime("10:00", "%H:%M")
        middya_thresh = datetime.strptime("14:00", "%H:%M")
        pm_thresh = datetime.strptime("19:00", "%H:%M")

        peak_hour_start = str(peak_hour).split("-")[0]
        peak_hour_start = datetime.strptime(peak_hour_start, "%H:%M")

        if peak_hour_start < am_thresh:
            return "AM"
        elif am_thresh <= peak_hour_start < middya_thresh:
            return "MiddayPeak"
        elif middya_thresh <= peak_hour_start < pm_thresh:
            return "PM"
        else:
            return "EveningPeak"

    def __process_link_segments(self, links_segments_list_dict):

        seasonality_dict = {}
        final_rows = []
        for key in links_segments_list_dict.keys():

            # link_id and day and month are unique
            link_id, day, month, year, is_weekday, is_public_holidays, is_school_holidays = key
            time_set_average_travel_time_list_list = links_segments_list_dict[key]

            # on weekends we only have one peak hour
            # for other days, we will have obe peak hour for am and
            # one for pm
            if not is_weekday:
                peak_hour_day_time = "WeekendPeak"

            peak_hour_finder = PeakHourExtractor(time_set_average_travel_time_list_list, is_weekday)

            peaks = peak_hour_finder.get_peaks()
            averages = peak_hour_finder.get_average_travel_times(peaks[0], peaks[1], peaks[2], peaks[3])
            step = 2
            peak_hour_day_time = "WeekendPeak"
            for index in range(0, int(len(peaks)/2), step):

                if peaks[index] is None:
                    continue

                if peaks[2] is not None:
                    #peak_hour_day_time = 'AM' if index == 0 else 'PM'
                     peak_hour_day_time = self.get_day_time(peaks[index])

                row = [link_id, day, month, year, is_weekday, is_public_holidays, is_school_holidays,
                       peaks[index], peaks[index + 1], peaks[index + 4], peaks[index + 5],
                       averages[index * 2], averages[index * 2 + 1],
                       averages[index * 2 + 2], averages[index * 2 + 3],
                       peak_hour_day_time]

                final_rows.append(row)

                seasonality_key = (link_id, day, peak_hour_day_time)

                if seasonality_key not in list(seasonality_dict.keys()):
                    seasonality_dict[seasonality_key] = []

                seasonality_dict[seasonality_key].append([peaks[index], peaks[index + 1], peak_hour_day_time])

        seasonality_dict = self.get_seasonality_averages(seasonality_dict)

        for row in final_rows:
            link_id = row[0]
            day = row[1]
            peak_hour = row[7]
            peak_interval = row[8]
            day_time = row[-1]
            peak_hour_average, peak_interval_average = seasonality_dict[(link_id, day, day_time)]
            peak_hour_seasonality, peak_interval_seasonality = self.get_seasonalities(peak_hour_average,
                                                                                     peak_interval_average,
                                                                                     peak_hour,
                                                                                     peak_interval)
            row.append(peak_hour_seasonality)
            row.append(peak_interval_seasonality)
            local_board, area, direction = self.__area_reader.get_localBaord_area_direction(link_id)
            row.append(local_board)
            row.append(area)
            row.append(direction)

            self.__append_to_export_columns_dict(row)

    def read_from_database(self):
        for day_abbr in self.__day_json_files_dict.keys():

            db_path = str(self.__jsons_root_folder_path)+"/"+str(day_abbr)+"/"+str(day_abbr)+".db"
            if not os.path.exists(db_path):
                print("DB path does not exist: ", db_path)
                continue
            print("Reading form db with path: ", db_path)

            database_wrapper = DatabaseWrapper(db_path, False)
            now = time.time()
            day_result = database_wrapper.fetch_all_segment_data()
            end = time.time()
            print("took :", end - now)
            self.__process_link_segments(day_result)

        self.__excel_exporter.write(self.__export_columns_dict)



    def read_json_files(self):

        self.__links_segments_ids_dict = self.__links_file_reader.get_links_dict()

        for day_abbr in self.__day_json_files_dict.keys():
            json_files_list = self.__day_json_files_dict[day_abbr]

            links_segments_list_dict = {}
            db_path = str(self.__jsons_root_folder_path)+"/"+str(day_abbr)+"/"+str(day_abbr)+".db"
            database_wrapper = DatabaseWrapper(db_path)

            for file_index, file_path in enumerate(json_files_list):

                print("file path ", file_path, " : ", file_index + 1, " / ", len(json_files_list))
                if "Dec" in file_path or "Jan" in file_path:
                    print("January and December are ignred")
                    continue

                # progress_value = int((file_index + 1) / len(json_files_list) * 100)
                # self.progress_value_changed.emit(progress_value)
                now = time.time()

                with open(file_path, 'rb') as file:

                    objects = ijson.items(file, '')

                    for obj in objects:
                        date_ranges = obj.get('dateRanges')

                        times_sets_dict = {}

                        time_sets = obj.get('timeSets')
                        for time_set in time_sets:
                            times_sets_dict[time_set["@id"]] = time_set["name"]

                        network = obj.get('network', {})
                        segment_results = network.get('segmentResults', [])
                        #print("len", len(times_sets_dict))

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
                            name = str(dr['name'])
                            # name = re.sub(r'[^a-zA-Z0-9]', '-', name)
                            name = name.replace("_", "-")
                            name = name.replace("- ", "-")
                            day = str(name.split(" ")[0]).split("-")[0]
                            # there are some typos in the name o
                            day = self.__date_time_manager.refine_day_name(day)
                            month = str(name.split(" ")[0]).split("-")[-1]
                            year = name.split(" ")[1]
                            # date_range = date_from + " to " + date_to
                            is_public_holidays = self.__holidays_manager.is_public_holiday(year, month, day)
                            is_school_holidays = self.__holidays_manager.is_school_holiday(year, month, day)
                            # is_day_after_public_holiday = self.__holidays_manager.is_day_after_holiday(year, month, day)
                            # is_day_before_public_holiday = self.__holidays_manager.is_day_before_holiday(year, month, day)
                            is_weekend = self.__holidays_manager.is_weekend(day)
                            is_weekday = not is_weekend

                        for segment in segment_results:

                            segment_id = segment['segmentId']

                            segment_id_is_valid = False

                            for link_id in self.__links_segments_ids_dict.keys():

                                # if link_id != "C036-C061":
                                #     continue

                                segment_ids_list = self.__links_segments_ids_dict[link_id]

                                if segment_id in segment_ids_list:
                                    # if link_id == "0092-0091":
                                    #     print("Segment id: ", segment_id)
                                    segment_id_is_valid = True
                                    break
                            if not segment_id_is_valid:
                                continue

                            time_set_average_travel_time_list = []
                            segment_time_results_list = segment.get('segmentTimeResults')
                            #print("Segment id ", segment['segmentId'])
                            for segment_time in segment_time_results_list:
                                time_set_id = segment_time["timeSet"]
                                time_set = times_sets_dict[time_set_id]
                                average_travel_time = segment_time['averageTravelTime']
                                #print("id ", time_set_id, " time set ", time_set, " average_travel_time ", average_travel_time)

                                #time_set_average_travel_time_list.append((time_set, average_travel_time))

                                key = (link_id, day, month, year, is_weekday, is_public_holidays, is_school_holidays)

                                if key not in links_segments_list_dict.keys():
                                    links_segments_list_dict[key] = []

                                links_segments_list_dict[key].append((time_set, average_travel_time))

                file.close()
                end = time.time()
                print("took :", end - now)

            #self.__database_wrapper.insert_into_database(links_segments_list_dict)
            database_wrapper.insert_into_database(links_segments_list_dict)
            #print("inserted in the database")
            #result = self.__database_wrapper.fetch_all_segment_data()
            #print(len(result))
            self.__process_link_segments(links_segments_list_dict)

        self.__excel_exporter.write(self.__export_columns_dict)

    def __init_export_columns_dict(self):

        for column in self.__export_columns:
            self.__export_columns_dict[column] = []

    def __init_export_columns(self):
        self.__export_columns = ['Link_id', 'Time',
                                 'Peak_hour', 'Peak_hour_quarter',
                                 'Average_travel_time_peak_hour', 'Peak_hour_MPHF', 'Peak_hour_seasonality',
                                 'Peak_period', 'Peak_period_quarter',
                                 'Average_travel_time_peak_period', 'Peak_period_MPHF', 'Peak_period_seasonality',
                                 'Day', 'Month', 'Year', 'Public_holidays', 'School_Term', 'Weekday', 'LocalBoard',
                                 'Area', 'Direction']

    def __append_to_export_columns_dict(self, row):
        # link_id, day, month, year, is_weekday, is_public_holidays, is_school_holidays,
        # peak_hour, peak_interval, peak_hour_average_travel_time, peak_interval_average_travel_time,
        # peak_hour_MPHF, peak_interval_MPHF, peak_hour_day_time,

        link_id = row[0]
        day = row[1]
        month = row[2]
        year = row[3]
        is_weekday = row[4]
        is_public_holidays = row[5]
        is_school_terms = row[6]
        peak_hour = row[7]
        peak_interval = row[8]
        peak_hour_quarter = row[9]
        peak_period_quarter = row[10]
        peak_hour_average_travel_time = row[11]
        peak_interval_average_travel_time = row[12]
        peak_hour_MPHF = row[13]
        peak_interval_MPHF = row[14]
        time = row[15]
        peak_hour_seasonality = row[16]
        peak_interval_seasonality = row[17]
        local_board = row[18]
        area = row[19]
        direction = row[20]

        self.__export_columns_dict[self.__export_columns[0]].append(link_id)
        self.__export_columns_dict[self.__export_columns[1]].append(time)
        self.__export_columns_dict[self.__export_columns[2]].append(peak_hour)
        self.__export_columns_dict[self.__export_columns[3]].append(peak_hour_quarter)

        self.__export_columns_dict[self.__export_columns[4]].append(peak_hour_average_travel_time)
        self.__export_columns_dict[self.__export_columns[5]].append(peak_hour_MPHF)
        self.__export_columns_dict[self.__export_columns[6]].append(peak_hour_seasonality)
        self.__export_columns_dict[self.__export_columns[7]].append(peak_interval)
        self.__export_columns_dict[self.__export_columns[8]].append(peak_period_quarter)

        self.__export_columns_dict[self.__export_columns[9]].append(peak_interval_average_travel_time)
        self.__export_columns_dict[self.__export_columns[10]].append(peak_interval_MPHF)
        self.__export_columns_dict[self.__export_columns[11]].append(peak_interval_seasonality)
        self.__export_columns_dict[self.__export_columns[12]].append(day)
        self.__export_columns_dict[self.__export_columns[13]].append(month)
        self.__export_columns_dict[self.__export_columns[14]].append(year)
        self.__export_columns_dict[self.__export_columns[15]].append(is_public_holidays)
        self.__export_columns_dict[self.__export_columns[16]].append(is_school_terms)
        self.__export_columns_dict[self.__export_columns[17]].append(is_weekday)
        self.__export_columns_dict[self.__export_columns[18]].append(local_board)
        self.__export_columns_dict[self.__export_columns[19]].append(area)
        self.__export_columns_dict[self.__export_columns[20]].append(direction)
