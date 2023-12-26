import pandas as pd
from enum import Enum


class TimeType(Enum):
    AM = 0
    PM = 1

class PeakHourExtractor:
    def __init__(self, tyme_type):
        self.__am_time_sets = {2: '5:00', 3: '5:15', 4: '5:30', 5: '5:45', 6: '6:00', 7: '6:15', 8: '6:30', 9: '6:45',
                               10: '7:00', 11: '7:15', 12: '7:30', 13: '7:45', 14: '8:00', 15: '8:15', 16: '8:30',
                               17: '8:45', 18: '9:00', 19: '9:15', 20: '9:45', 21: '10:00'}
        self.__timeset_travel_time_dict = {}

        self.__slide_window_size = 4

        self.__sum_values = []

        self.__peak_hour_index = -1

        self.__time_type = tyme_type

        self.__peak_hour_time_set = -1

    def calculate_peak_period(self):

        number_of_segments = int(len(self.__am_time_sets) / self.__slide_window_size)
        sum_values_list = []
        time_travel_values = list(self.__timeset_travel_time_dict.values())

        for index in range(0, number_of_segments):
            start = index * self.__slide_window_size
            start = min(start, len(time_travel_values))

            end = start + self.__slide_window_size
            end = min(end, len(time_travel_values))

            range_values = list(time_travel_values[start:end])
            sum_values_list.append(sum(range_values))

        sum_values_list_sorted = sum_values_list.copy()
        sum_values_list_sorted.sort(reverse=True)

        sum_values_list_sorted_indices = self.__find_indices(sum_values_list_sorted, sum_values_list_sorted)

        for index in range(0, number_of_segments):

            start = index * self.__slide_window_size

            end = start + self.__slide_window_size
            end = min(end, len(self.__am_time_sets)-1)

            if start <= self.__peak_hour_index < end:
                time_sets = list(self.__am_time_sets.keys())
                time_set_start = time_sets[start]
                time_set_end = time_sets[end]
                period = self.__am_time_sets[time_set_start] + " to " + self.__am_time_sets[time_set_end]

                return period
    def calculate_peak_hour(self, segment_time_result):

        #extract median travel time of each time set and save in a dict
        for segment_time in segment_time_result:
            median_travel_time = segment_time['medianTravelTime']
            time_set = segment_time['timeSet']
            self.__timeset_travel_time_dict[time_set] = median_travel_time
        # get the travel times for future uses
        time_travel_values = list(self.__timeset_travel_time_dict.values())

        # for each median travel time, extract the values from current index to 4 index ahead
        # that comprises one hour
        for index in range(0, len(self.__am_time_sets)):

            # this is the start index of each hour(4 quarters)
            start = index
            end = index + 4
            # bound the end value to the range ot the list
            end = min(end, len(self.__am_time_sets))

            #extract current index to one hour ahead
            one_hour_values = time_travel_values[start: end]

            #sum the values
            sum_time_travel = sum(one_hour_values)

            # save 1-hour sums
            self.__sum_values.append(sum_time_travel)

        # find the 3 maximum sum values
        sorted_sum_values = self.__sum_values.copy()
        sorted_sum_values.sort(reverse=True)

        #highest_3_values contains the 3 highest sums
        highest_3_values = sorted_sum_values[0:3]
        return self.__return_peak_of_3_highest(time_travel_values, self.__sum_values, highest_3_values)


    def __get_all_indices(self, lst, value):
        return [index for index, elem in enumerate(lst) if elem == value]

    def __find_indices(self, input_list, main_list):
        checked_values = []
        values_indices = []
        for index, item in enumerate(input_list):
            if item not in checked_values:
                indices = self.__get_all_indices(main_list, item)
                for idx in indices:
                    values_indices.append(idx )
                checked_values.append(item)
        return values_indices

    def __return_peak_of_3_highest(self, time_travel_values, sum_values, highest_3_values):

        previous_and_next_sum_list = []
        highest_sum_indices = self.__find_indices(highest_3_values, sum_values)
        for index, highest in enumerate(highest_3_values):

            highest_sum_index = highest_sum_indices[index]
            previous_3_start = highest_sum_index-3
            previous_3_end = highest_sum_index

            previous_3_start = max(0, previous_3_start)
            previous_3_end = max(0, previous_3_end)

            next_3_start = highest_sum_index+1
            next_3_end = next_3_start+3

            next_3_start = min(next_3_start, len(time_travel_values)-1)
            next_3_end = min(next_3_end, len(time_travel_values))

            previous_values_sum = sum(time_travel_values[previous_3_start:previous_3_end])
            next_values_sum = sum(time_travel_values[next_3_start:next_3_end])

            previous_and_next_sum_list.append(previous_values_sum+next_values_sum)

        # highest_3_values and previous_and_next_sum_list have the same size
        previous_and_next_sum_list_sorted = previous_and_next_sum_list.copy()
        previous_and_next_sum_list_sorted.sort(reverse=True)

        maximum_previous_and_next_sum_indices = self.__find_indices(previous_and_next_sum_list_sorted,
                                                                    previous_and_next_sum_list)

        for maximum_sum_index in maximum_previous_and_next_sum_indices:

            highest_value_index = highest_sum_indices[maximum_sum_index]

            # decide if the time set is for 5:00 to 5:45. if it was, we ignore it
            # 3 is the index of 5:45
            if self.__time_type == TimeType.AM and highest_value_index > 3:
                time_sets = list(self.__am_time_sets.keys())
                self.__peak_hour_time_set = time_sets[highest_value_index]

                self.__peak_hour_index = highest_value_index
                peak_hour = self.__am_time_sets[self.__peak_hour_time_set]
                return


