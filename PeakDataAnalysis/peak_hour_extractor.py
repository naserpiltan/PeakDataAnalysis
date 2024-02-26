import pandas as pd
from enum import Enum
from datetime import datetime, timedelta
from functools import reduce


class TimeType(Enum):
    AM = 0
    PM = 1


class PeakHourExtractor:
    def __init__(self, time_set_average_travel_time_list_list, is_weekday):

        self.__time_sets = {}

        self.__timeset_travel_time_dict = {}

        self.__slide_window_size = 4

        self.__sum_values = []

        self.__peak_hour_index = -1

        self.__peak_hour_time_set = -1

        self.__segment_time_result = None

        self.__time_set_average_travel_time_list_list = time_set_average_travel_time_list_list

        self.__reliable_speed_threshold = 5  #

        self.__precentile_lower_bound = 0  # 5th

        self.__precentile_upper_bound = 18  # 95th

        self.__reliable_percentile_threshold = 5

        self.__time_set_travel_times = {}

        self.__sum_travel_times = {}

        self.__peak_hour_mphf = 0

        self.__peak_interval_mphf = 0

        self.__is_week_day = is_weekday

        self.__init_time_sets()

        self.get_travel_times()

    def __get_all_indices(self, lst, value):
        return [index for index, elem in enumerate(lst) if elem == value]

    def __find_indices(self, input_list, main_list):
        checked_values = []
        values_indices = []
        for index, item in enumerate(input_list):
            if item not in checked_values:
                indices = self.__get_all_indices(main_list, item)
                for idx in indices:
                    values_indices.append(idx)
                checked_values.append(item)
        return values_indices

    def is_sample_size_reliable(self):

        # if __peak_hour_index equals to -1, sample size is not reliable
        if self.__peak_hour_index == -1:
            return False
        sample_size = self.__segment_time_result[self.__peak_hour_index]['sampleSize']
        return sample_size > self.__reliable_speed_threshold

    def is_percentile_reliable(self):

        # if __peak_hour_index equals to -1, sample size is not reliable
        if self.__peak_hour_index == -1:
            return False

        precentile_list = self.__segment_time_result[self.__peak_hour_index]['speedPercentiles']

        # get the diff between 5th and 95th speedPercentiles difference
        percentile_diff = abs(int(precentile_list[self.__precentile_upper_bound]) -
                              int(precentile_list[self.__precentile_lower_bound]))
        return percentile_diff > self.__reliable_percentile_threshold

    def get_peak_period_1_hour_a(self):

        # each 4 time sets represent one hour
        slider_window_size = self.__slide_window_size
        return self.calculate_peak_period(slider_window_size)

    def get_peak_period_2_hour_a(self):

        # operations are done inside two hours
        slider_window_size = 2 * self.__slide_window_size
        return self.calculate_peak_period(slider_window_size)

    def calculate_peak_period(self, slider_window_size):

        number_of_segments = int((len(self.__time_sets) - 1) / slider_window_size) + 1
        sum_values_list = []
        time_travel_values = list(self.__timeset_travel_time_dict.values())

        for index in range(0, number_of_segments):
            start = index * slider_window_size
            start = min(start, len(time_travel_values))

            end = start + slider_window_size
            end = min(end, len(time_travel_values))

            range_values = list(self.__sum_values[start:end])
            sum_values_list.append(sum(range_values))

        for segment_index in range(0, number_of_segments):

            segment_start = segment_index * slider_window_size

            segment_end = segment_start + slider_window_size
            segment_end = min(segment_end, len(self.__time_sets) - 1)

            if segment_start <= self.__peak_hour_index < segment_end:
                time_sets = list(self.__time_sets.keys())
                time_set_start = time_sets[segment_start]
                time_set_end = time_sets[segment_end]
                period = self.__time_sets[time_set_start] + " to " + self.__time_sets[time_set_end]
                return period

        return "- to -"

    def get_peak_period_1_hour_b(self):

        sum_values_list = []

        time_travel_values = list(self.__timeset_travel_time_dict.values())

        # this time we move by two steps
        for index in range(0, len(self.__time_sets), 2):
            # this is the start index of each hour(4 quarters)
            start = index
            end = index + self.__slide_window_size
            # bound the end value to the range ot the list
            end = min(end, len(self.__time_sets))

            # extract current index to one hour ahead
            one_hour_values = time_travel_values[start: end]

            sum_values_list.append(sum(one_hour_values))

        for segment_index in range(0, len(sum_values_list)):

            start = segment_index * 2
            end = start + self.__slide_window_size
            end = min(end, len(self.__time_sets) - 1)

            if start <= self.__peak_hour_index < end:
                time_sets = list(self.__time_sets.keys())
                time_set_start = time_sets[start]
                time_set_end = time_sets[end]
                period = self.__time_sets[time_set_start] + " to " + self.__time_sets[time_set_end]
                return period

        return "- to -"

    def get_peak_hour_index(self):
        return self.__peak_hour_index

    def calculate_peak_hour(self):
        # extract median travel time of each time set and save in a dict
        for segment_time in self.__segment_time_result:
            median_travel_time = segment_time['medianTravelTime']
            time_set = segment_time['timeSet']
            self.__timeset_travel_time_dict[time_set] = median_travel_time
        # get the travel times for future uses
        time_travel_values = list(self.__timeset_travel_time_dict.values())

        # for each median travel time, extract the values from current index to 4 index ahead
        # that comprises one hour
        for index in range(0, len(self.__time_sets)):
            # this is the start index of each hour(4 quarters)
            start = index
            end = index + self.__slide_window_size
            # bound the end value to the range ot the list
            end = min(end, len(self.__time_sets))

            # extract current index to one hour ahead
            one_hour_values = time_travel_values[start: end]

            # sum the values
            sum_time_travel = sum(one_hour_values)

            # save 1-hour sums
            self.__sum_values.append(sum_time_travel)

        # find the 3 maximum sum values
        sorted_sum_values = self.__sum_values.copy()
        sorted_sum_values.sort(reverse=True)

        # highest_3_values contains the 3 highest sums
        highest_3_values = sorted_sum_values[0:3]
        return self.__return_peak_of_3_highest(time_travel_values, self.__sum_values, highest_3_values)

    def __return_peak_of_3_highest(self, time_travel_values, sum_values, highest_3_values):
        previous_and_next_sum_list = []
        highest_sum_indices = self.__find_indices(highest_3_values, sum_values)
        for index, highest in enumerate(highest_3_values):
            highest_sum_index = highest_sum_indices[index]
            previous_3_start = highest_sum_index - 3
            previous_3_end = highest_sum_index

            previous_3_start = max(0, previous_3_start)
            previous_3_end = max(0, previous_3_end)

            next_3_start = highest_sum_index + 1
            next_3_end = next_3_start + 3

            next_3_start = min(next_3_start, len(time_travel_values) - 1)
            next_3_end = min(next_3_end, len(time_travel_values))

            previous_values_sum = sum(time_travel_values[previous_3_start:previous_3_end])
            next_values_sum = sum(time_travel_values[next_3_start:next_3_end])

            previous_and_next_sum_list.append(previous_values_sum + next_values_sum)

        # highest_3_values and previous_and_next_sum_list have the same size
        previous_and_next_sum_list_sorted = previous_and_next_sum_list.copy()
        previous_and_next_sum_list_sorted.sort(reverse=True)

        maximum_previous_and_next_sum_indices = self.__find_indices(previous_and_next_sum_list_sorted,
                                                                    previous_and_next_sum_list)

        for maximum_sum_index in maximum_previous_and_next_sum_indices:
            highest_value_index = highest_sum_indices[maximum_sum_index]

            time_sets = list(self.__time_sets.keys())
            self.__peak_hour_time_set = time_sets[highest_value_index]

            self.__peak_hour_index = highest_value_index
            peak_hour = self.__time_sets[self.__peak_hour_time_set]
            return peak_hour

        return -1

    def __init_time_sets(self):

        # Adjusted starting and ending times for 24-hour format
        start_time = datetime.strptime("05:00", "%H:%M")
        end_time = datetime.strptime("22:00", "%H:%M")  # 10:00 PM in 24-hour format

        # Increment of 15 minutes
        time_increment = timedelta(minutes=15)

        # Generate time list using a for loop
        current_time = start_time
        time_set_index = 2
        while current_time <= end_time:
            next_time = current_time + time_increment

            time_set = current_time.strftime("%H:%M") + "-" + next_time.strftime("%H:%M")

            self.__time_sets[time_set_index] = time_set

            self.__time_set_travel_times[time_set] = []

            self.__sum_travel_times[time_set] = []

            current_time = next_time

            time_set_index += 1

    def average(self, lst):
        if len(lst) == 0:
            return 0
        return sum(lst) / len(lst)

    def get_travel_times(self):

        morning_thresh = datetime.strptime("09:00", "%H:%M")
        middya_thresh = datetime.strptime("14:00", "%H:%M")
        night_thresh = datetime.strptime("18:00", "%H:%M")

        # all the segments of a link
        for index, time_set_average_travel_time_list_list in enumerate(self.__time_set_average_travel_time_list_list):

            for (time_set, average_travel_time) in time_set_average_travel_time_list_list:

                start_time = time_set.split('-')[0]

                start_time = datetime.strptime(str(start_time), "%H:%M")

                # if time set is between 10 and 14 or is bigger than 19 it must be discarded
                # if (morning_thresh <= start_time < middya_thresh) or start_time > night_thresh:
                #     continue

                time_increment = timedelta(minutes=15)

                next_time = start_time + time_increment

                time_set_value = start_time.strftime("%H:%M") + "-" + next_time.strftime("%H:%M")

                self.__time_set_travel_times[time_set_value].append(average_travel_time)

        sum_travel_times = []
        for time_set_value in self.__time_set_travel_times.keys():
            travel_times = self.__time_set_travel_times[time_set_value]

            # sum_travel_times.append(travel_times_average)
            self.__sum_travel_times[time_set_value] = sum(travel_times)

    def __get_peak(self, sum_travel_times_dict, slider_size, day_time="WeekendPeak"):
        sum_travel_times_list = list(sum_travel_times_dict.values())

        sum_sum_travel_times_list = []
        for index, value in enumerate(sum_travel_times_list):
            start = index
            end = index + slider_size
            # bound the end value to the range ot the list
            end = min(end, len(sum_travel_times_list))

            av = sum_travel_times_list[start:end]

            sum_average_travel_times = sum(av)

            sum_sum_travel_times_list.append(sum_average_travel_times)

        start_index = 0
        end_index = len(sum_sum_travel_times_list)

        middle_day = datetime.strptime("12:00", "%H:%M")
        time_increment = timedelta(minutes=15)
        next_time = middle_day + time_increment
        middle_day = middle_day.strftime("%H:%M") + "-" + next_time.strftime("%H:%M")

        middle_day_index = list(sum_travel_times_dict.keys()).index(middle_day)
        if day_time == "AM":
            end_index = middle_day_index
        elif day_time == "PM":
            start_index = middle_day_index

        max_value = max(sum_sum_travel_times_list[start_index:end_index])
        max_index = sum_sum_travel_times_list.index(max_value, start_index, end_index)

        max_quarter = max(sum_travel_times_list[max_index:min(max_index+slider_size, len(sum_travel_times_list))])
        max_quarter_index = sum_travel_times_list.index(max_quarter)
        max_time_set = list(sum_travel_times_dict.keys())[max_index]
        max_time_set_quarter = list(sum_travel_times_dict.keys())[max_quarter_index]

        start_time_set = str(max_time_set).split("-")[0]

        start_time = datetime.strptime(start_time_set, "%H:%M")

        # Increment of 15 minutes
        time_increment = timedelta(minutes=slider_size * 15)

        next_time = start_time + time_increment

        peak_hour = start_time.strftime("%H:%M") + "-" + next_time.strftime("%H:%M")

        # self.__peak_hour_time_set = start_time_set

        return peak_hour, max_time_set_quarter

    def get_peaks(self):

        if self.__is_week_day:
            am_peak_hour, am_peak_hour_quarter = self.__get_peak(self.__sum_travel_times, self.__slide_window_size, "AM")
            pm_peak_hour, pm_peak_hour_quarter = self.__get_peak(self.__sum_travel_times, self.__slide_window_size, "PM")
            am_peak_period, am_peak_per_quarter = self.__get_peak(self.__sum_travel_times, self.__slide_window_size * 2, "AM")
            pm_peak_period, pm_peak_per_quarter = self.__get_peak(self.__sum_travel_times, self.__slide_window_size * 2,"PM")
            return (am_peak_hour, am_peak_period,
                    pm_peak_hour, pm_peak_period,
                    am_peak_hour_quarter, am_peak_per_quarter,
                    pm_peak_hour_quarter, pm_peak_per_quarter)

        else:
            peak_hour, peak_hour_quarter = self.__get_peak(self.__sum_travel_times, self.__slide_window_size)
            peak_period, peak_per_quarter = self.__get_peak(self.__sum_travel_times, self.__slide_window_size * 2)
            return (peak_hour, peak_period,
                    None,None,
                    peak_hour_quarter, peak_per_quarter,
                    None,None)

    def __get_peak_interval(self, sum_travel_times_dict):
        sum_travel_times_list = list(sum_travel_times_dict.values())

        sum_sum_travel_times_list = []
        for index, value in enumerate(sum_travel_times_list):
            start = index
            end = index + self.__slide_window_size * 2
            # bound the end value to the range ot the list
            end = min(end, len(sum_travel_times_list))

            sum_average_travel_times = sum(sum_travel_times_list[start:end])

            sum_sum_travel_times_list.append(sum_average_travel_times)

        max_value = max(sum_sum_travel_times_list)
        max_index = sum_sum_travel_times_list.index(max_value)

        max_time_set = list(sum_travel_times_dict.keys())[max_index]

        start_time_set = str(max_time_set).split("-")[0]

        start_time = datetime.strptime(start_time_set, "%H:%M")

        # Increment of 15 minutes
        time_increment = timedelta(minutes=120)

        next_time = start_time + time_increment

        peak_interval = start_time.strftime("%H:%M") + "-" + next_time.strftime("%H:%M")

        return peak_interval

    def get_peak_interval(self):
        pass

    def __get_average_travel_times(self, peak_time, times_sets_list, sum_travel_times_list, slider_size):
        start_time_set = str(peak_time).split("-")[0]

        start_time = datetime.strptime(str(start_time_set), "%H:%M")
        time_increment = timedelta(minutes=15)
        next_time = start_time + time_increment

        time_set = start_time.strftime("%H:%M") + "-" + next_time.strftime("%H:%M")

        index_of_times_set = times_sets_list.index(time_set)

        peak_sum_travel_times = []
        for index in range(index_of_times_set, index_of_times_set + slider_size):
            if index < len(sum_travel_times_list):
                avera_travel_time = sum_travel_times_list[index]
                peak_sum_travel_times.append(avera_travel_time)

        average = self.average(peak_sum_travel_times)

        peak__mphf = sum(peak_sum_travel_times)
        max_peak_sum = max(peak_sum_travel_times)
        if max_peak_sum > 0:
            peak__mphf = peak__mphf / (slider_size * max_peak_sum)
        else:
            peak__mphf = 0

        return average, peak__mphf

    def get_average_travel_times(self, am_peak_hour, am_peak_period, pm_peak_hour: None, pm_peak_period: None):

        am_time_sets_list = []
        pm_time_sets_list = []
        am_sum_travel_times_list = []
        pm_sum_travel_times_list = []


        # for time_set in list(self.__sum_travel_times.keys()):
        #     start_time_set = str(time_set).split("-")[0]
        #     start_time = datetime.strptime(start_time_set, "%H:%M")
        #     if start_time.hour < middle_day.hour:
        #         am_time_sets_list.append(time_set)
        #         am_sum_travel_times_list.append(self.__sum_travel_times[time_set])
        #     else:
        #         pm_time_sets_list.append(time_set)
        #         pm_sum_travel_times_list.append(self.__sum_travel_times[time_set])
        time_sets_list = list(self.__sum_travel_times.keys())
        average_travel_times_list = list(self.__sum_travel_times.values())
        if self.__is_week_day:
            # am_peak_hour_average_travel_time, am_peak_hour_mphf
            am_p_h_a_t_t, am_p_h_mphf = self.__get_average_travel_times(am_peak_hour,
                                                                        time_sets_list,
                                                                        average_travel_times_list,
                                                                        self.__slide_window_size)
            # am_peak_period_average_travel_time, am_peak_period_mphf
            am_p_p_a_t_t, am_p_p_mphf = self.__get_average_travel_times(am_peak_period,
                                                                        time_sets_list,
                                                                        average_travel_times_list,
                                                                        2 * self.__slide_window_size)

            # pm_peak_hour_average_travel_time, pm_peak_hour_mphf
            pm_p_h_a_t_t, p_p_h_mphf = self.__get_average_travel_times(pm_peak_hour,
                                                                       time_sets_list,
                                                                       average_travel_times_list,
                                                                       self.__slide_window_size)
            # pm_peak_period_average_travel_time, pm_peak_period_mphf
            pm_p_p_a_t_t, pm_p_p_mphf = self.__get_average_travel_times(pm_peak_period,
                                                                        time_sets_list,
                                                                        average_travel_times_list,
                                                                        2 * self.__slide_window_size)
            return (am_p_h_a_t_t, am_p_p_a_t_t, am_p_h_mphf, am_p_p_mphf,
                    pm_p_h_a_t_t, pm_p_p_a_t_t, p_p_h_mphf, pm_p_p_mphf)

        else:

            # peak_hour_average_travel_time, peak_hour_mphf
            p_h_a_t_t, p_h_mphf = self.__get_average_travel_times(am_peak_hour,
                                                                  time_sets_list,
                                                                  average_travel_times_list,
                                                                  self.__slide_window_size)
            # peak_period_average_travel_time, peak_period_mph
            p_p_a_t_t, p_p_mphf = self.__get_average_travel_times(am_peak_period,
                                                                  time_sets_list,
                                                                  average_travel_times_list,
                                                                  2 * self.__slide_window_size)
            return p_h_a_t_t, p_p_a_t_t, p_h_mphf, p_p_mphf, None, None,None,None

    def get_peak_interval_average_travel_time(self):
        time_sets_list = list(self.__sum_travel_times.keys())

        average_travel_times_list = list(self.__sum_travel_times.values())

        start_time_set = self.__peak_hour_time_set

        start_time = datetime.strptime(str(start_time_set), "%H:%M")
        time_increment = timedelta(minutes=15)
        next_time = start_time + time_increment

        time_set = start_time.strftime("%H:%M") + "-" + next_time.strftime("%H:%M")

        index_of_times_set = time_sets_list.index(time_set)

        peak_interval_travel_times = []
        for index in range(index_of_times_set, index_of_times_set + self.__slide_window_size * 2):
            if index < len(average_travel_times_list):
                avera_travel_time = average_travel_times_list[index]
                peak_interval_travel_times.append(avera_travel_time)

        average = self.average(peak_interval_travel_times)

        peak_interval_mphf = sum(peak_interval_travel_times)
        max_peak_interval_sum = max(peak_interval_travel_times)
        peak_interval_mphf = peak_interval_mphf / (self.__slide_window_size * 2 * max_peak_interval_sum)
        self.__peak_interval_mphf = peak_interval_mphf

        return average

    def get_peak_hour_day_time(self):
        time = datetime.strptime(str(self.__peak_hour_time_set), "%H:%M")
        return "AM" if time.hour < 12 else "PM"

    def get_peak_hour_MPHF(self):
        return self.__peak_hour_mphf

    def get_peak_interval_MPHF(self):
        return self.__peak_interval_mphf


if __name__ == "__main__":
    segment_result = []
    peak_hour_extractor = PeakHourExtractor(segment_result)
