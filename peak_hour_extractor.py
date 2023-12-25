import pandas as pd


class PeakHourExtractor:
    def __init__(self):
        self.__am_time_sets = {2: '5:00', 3: '5:15', 4: '5:30', 5: '5:45', 6: '6:00', 7: '6:15', 8: '6:30', 9: '6:45',
                               10: '7:00', 11: '7:15', 12: '7:30', 13: '7:45', 14: '8:00', 15: '8:15', 16: '8:30',
                               17: '8:45', 18: '9:00', 19: '9:15', 20: '9:45', 21: '10:00'}
        self.__timeset_travel_time_dict = {}

        self.__slide_window_size = 4

        self.__sum_values = []

        self.__peak_hour_index = None

    def calculate_peak_period(self):

        number_of_segments = int(len(self.__am_time_sets) / self.__slide_window_size + 1)

        aggregated_sum_values = []
        for index in range(0, number_of_segments):
            start = index * self.__slide_window_size
            start = min(start, len(self.__am_time_sets))

            end = start + self.__slide_window_size
            end = min(end, len(self.__am_time_sets))

            aggregated_sum_values.append(self.__sum_values[start:end])

        for index in range(0, number_of_segments):
            start = index * self.__slide_window_size
            start = min(start, len(self.__am_time_sets))

            end = start + self.__slide_window_size
            end = min(end, len(self.__am_time_sets))

            if start <= self.__peak_hour_index < end:
                return aggregated_sum_values[start]

    def calculate_peak_hour(self, segment_time_result):
        for segment_time in segment_time_result:
            medianTravelTime = segment_time['medianTravelTime']
            timeSet = segment_time['timeSet']
            self.__timeset_travel_time_dict[timeSet] = medianTravelTime
        time_travel_values = self.__timeset_travel_time_dict.values()

        for index in range(0, len(self.__am_time_sets)):

            # this is the start index of each hour(4 quarters)
            start = index
            end = index + 4
            # bound the end value to the range ot the list
            if end > len(self.__am_time_sets):
                end = len(self.__am_time_sets)

            one_hour_values = time_travel_values[start: end]
            sum_time_travel = sum(one_hour_values)

            # aggregate 1-hour sum values
            self.__sum_values.append(sum_time_travel)

        # find the 3 maximum sum values
        sorted_sum_values = self.__sum_values
        sorted_sum_values.sort(reverse=True)
        highest_3_values = sorted_sum_values[0:3]
        return self.__return_peak_of_3_highest(time_travel_values, self.__sum_values, highest_3_values)

    def __return_peak_of_3_highest(self, time_travel_values, sum_values, highest_3_values):
        highest_1_index = sum_values[highest_3_values[0]]
        highest_2_index = sum_values[highest_3_values[1]]
        highest_3_index = sum_values[highest_3_values[2]]

        # find the sum of 3 travel_time after and vefor each maximum value
        highest_1_previous = highest_1_index - 3
        highest_2_previous = highest_2_index - 3
        highest_3_previous = highest_3_index - 3

        highest_1_next = highest_1_index + 3
        highest_2_next = highest_2_index + 3
        highest_3_next = highest_3_index + 3

        # bind values to the range of list
        highest_1_previous = max(0, highest_1_previous)

        highest_2_previous = max(0, highest_2_previous)

        highest_3_previous = max(0, highest_3_previous)

        highest_1_next = min(highest_1_next, len(time_travel_values))
        highest_2_next = min(highest_2_next, len(time_travel_values))
        highest_3_next = min(highest_3_next, len(time_travel_values))

        highest_1_previous_sum = sum(time_travel_values[highest_1_previous:highest_1_index])
        highest_1_next_sum = sum(time_travel_values[highest_1_index + 1:highest_1_next + 1])

        highest_2_previous_sum = sum(time_travel_values[highest_2_previous:highest_2_index])
        highest_2_next_sum = sum(time_travel_values[highest_2_index + 1:highest_2_next + 1])

        highest_3_previous_sum = sum(time_travel_values[highest_3_previous:highest_3_index])
        highest_3_next_sum = sum(time_travel_values[highest_3_index + 1:highest_3_next + 1])

        diff_list = [abs(highest_1_previous_sum + highest_1_next_sum), abs(highest_2_previous_sum + highest_2_next_sum),
                     abs(highest_3_previous_sum + highest_3_next_sum)]

        maximum_diff = max(diff_list)
        maximum_diff_index = diff_list.index(diff_list)

        return highest_3_values[maximum_diff_index]
