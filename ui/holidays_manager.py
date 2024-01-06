import pandas as pd
from date_time_manager import DateTimeManager
from datetime import datetime, timedelta
from multipledispatch import dispatch

class HolidaysManager:
    def __init__(self):
        self.__public_holidays_dict = {}
        self.__school_holidays_dict = {}
        self.__init_holidays()
        self.__date_time_manager = DateTimeManager()
        self.__public_holiday_indexes = None
        self.__school_holiday_indexes = None

    def set_holidays_indexes(self, public_holidays_indexes, school_holiday_indexes):
        self.__public_holiday_indexes = public_holidays_indexes
        self.__school_holiday_indexes = school_holiday_indexes

    def __init_holidays(self):
        self.__public_holidays_date_dict = {

            #christmass to day after new year has been integrated into one period
            'New Year Holidays 2022': (pd.to_datetime('2022-12-21'), pd.to_datetime('2023-1-8')),
            'Auckland Anniversary 2023': (pd.to_datetime('2023-1-27'), pd.to_datetime('2023-1-31')),
            'Waitangi Day 2023': (pd.to_datetime('2023-2-3'), pd.to_datetime('2023-2-7')),
            'Good Friday-Easter Monday': (pd.to_datetime('2023-4-6'), pd.to_datetime('2023-4-11')),
            'ANZAC Day': (pd.to_datetime('2023-4-21'), pd.to_datetime('2023-4-26')),
            'King\'s Birthday': (pd.to_datetime('2023-6-2'), pd.to_datetime('2023-6-6')),
            'Matariki': (pd.to_datetime('2023-7-13'), pd.to_datetime('2023-7-17')),
            'Labour Day': (pd.to_datetime('2023-10-20'), pd.to_datetime('2023-10-24')),
            'New Year Holidays 2023': (pd.to_datetime('2023-12-21'), pd.to_datetime('2024-1-8')),

        }

        self.__public_holidays_dict = {
            'New Year Holidays 2022': ["2022", "2023", "December", "January"], #these two months will be removed
            'Auckland Anniversary 2023': ["January", "Friday", "Saturday", "Sunday", "Monday", "Tuesday"],
            'Waitangi Day 2023': ["February", "Friday", "Saturday", "Sunday", "Monday", "Tuesday"],
            'Good Friday-Easter Monday 2023': ["April", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday"],
            'ANZAC Day 2023': ["April", "Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday"],
            'King\'s Birthday 2023': ["June", "Friday", "Saturday", "Sunday", "Monday", "Tuesday"],
            'Matariki': ['July', "Thursday", "Friday", "Saturday", "Sunday", "Monday"],
            'Labour Day 2023': ["October", "Friday", "Saturday", "Sunday", "Monday", "Tuesday"],
            'New Year Holidays 2023': ["2023", "2024", "January", "December"],
        }

        self.__school_holidays_date_dict = {
            'Term 4 Holidays, 2022': (pd.to_datetime('2022-12-21'), pd.to_datetime('2023-1-30')), # december
            'Term 1 Holidays, 2023': (pd.to_datetime('2023-04-07'), pd.to_datetime('2023-04-23')),
            'Term 2 Holidays, 2023': (pd.to_datetime('2023-07-1'), pd.to_datetime('2023-07-16')),
            'Term 3 Holidays, 2023': (pd.to_datetime('2023-09-23'), pd.to_datetime('2023-10-8')),
            'Term 4 Holidays, 2023': (pd.to_datetime('2023-12-20'), pd.to_datetime('2024-1-29')),
            'School start Term 1, 2023': (pd.to_datetime('2023-1-30'), pd.to_datetime('2023-2-07')),
            'School start Term 2, 2023': (pd.to_datetime('2023-4-24'), pd.to_datetime('2023-4-24')),
            'School start Term 3, 2023': (pd.to_datetime('2023-7-17'), pd.to_datetime('2023-7-17')),
            'School start Term 4, 2023': (pd.to_datetime('2023-10-09'), pd.to_datetime('2023-10-09')),

        }

        self.__school_holidays_dict = {

            'Term 4 Holidays, 2022': ["2022", "2023", "December", "January"],  # december
            'Term 1 Holidays, 2023': ["April"],# december - anuary - february wednsday
            'Term 2 Holidays, 2023': ["July"],
            'Term 3 Holidays, 2023': ['September', "October"],
            'Term 4 Holidays, 2023': ["2023", "2024", "December", "January"],
            'School start Term 1, 2023': ["January", "Monday", "Tuesday", " February"],
            'School start Term 2, 2023': ["April", "Monday"],
            'School start Term 3, 2023': ["April", "Monday"],
            'School start Term 4, 2023': ["April", "Monday"],
        }
    def __is_public_holiday(self, date):
        for start_date, end_date in self.__public_holidays_date_dict.values():
            #print("date:", date.date(), " holiday date:", holiday_date.date(), " status:", date.date() == holiday_date.date())
            if start_date <= date <= end_date:
                return True
        return False

    def is_public_holiday(self, year, month_name, week_day_name):
        day_name = week_day_name
        if week_day_name[-1] == 's':
            day_name = week_day_name[:-1]
        month = self.__date_time_manager.month_name_to_index(month_name)
        dates = self.__date_time_manager.find_weekdays(year, month, day_name)
        #print("Dates: ",dates)
        for date in dates:
            if self.__is_public_holiday(pd.to_datetime(date)):
                return True
        return False

    def is_public_holiday_included(self, year, month_name, week_day_name):

        p_h_list = list(self.__public_holidays_dict.values())

        for p_h_index, p_h_state in enumerate(self.__public_holiday_indexes):
            if not p_h_state:
                continue

            # new year day
            if (p_h_index == 0 or p_h_index == 8) and month_name in p_h_list[p_h_index]:
                return False

            #other days
            if month_name in p_h_list[p_h_index] and week_day_name in p_h_list[p_h_index]:
                return False
        return True


    def is_school_holiday_included(self, year, month_name, week_day_name):

        s_h_list = list(self.__school_holidays_dict.values())

        for s_h_index, s_h_state in enumerate(self.__school_holiday_indexes):
            if not s_h_state:
                continue

            if (s_h_index == 0 or s_h_index == 1 or s_h_index == 2 or s_h_index == 3 or s_h_index == 4) and (month_name in s_h_list[s_h_index]):
                return False

            #School start Term 1, 2023 is not covered by the next case
            if s_h_index == 5 and month_name == "February":
                return False

            if month_name in s_h_list[s_h_index] and week_day_name in s_h_list[s_h_index]:
                return False
        return True

    # Function to check if a date is a school holiday
    def __is_school_holiday(self, date):
        for start_date, end_date in self.__school_holidays_date_dict.values():
            if start_date <= date <= end_date:
                return True
        return False

    def is_school_holiday(self, year, month_name, week_day_name):
        day_name = week_day_name
        if week_day_name[-1] == 's':
            day_name = week_day_name[:-1]
        month = self.__date_time_manager.month_name_to_index(month_name)
        dates = self.__date_time_manager.find_weekdays(year, month, day_name)
        for date in dates:
            if self.__is_school_holiday(pd.to_datetime(date)):
                return True
        return False

    def is_day_after_holiday(self, year, month_name, week_day_name):
        month = self.__date_time_manager.month_name_to_index(month_name)
        dates = self.__date_time_manager.find_weekdays(year, month, week_day_name)
        for date in dates:
            date = pd.to_datetime(date)
            day_before = date
            day_before += timedelta(days=-1)
            if self.__is_public_holiday(day_before):
                return True
        return False

    def is_day_before_holiday(self, year, month_name, week_day_name):
        month = self.__date_time_manager.month_name_to_index(month_name)
        dates = self.__date_time_manager.find_weekdays(year, month, week_day_name)
        for date in dates:
            date = pd.to_datetime(date)
            next_day = date
            #if we add one day to the current date and it turns out to be a holiday, so it is a day before holiday
            next_day += timedelta(days=1)
            if self.__is_public_holiday(next_day):
                return True
        return False

    def is_weekend(self, week_day_name):
        day_name = week_day_name
        if week_day_name[-1] == 's':
            day_name = week_day_name[:-1]
        return (self.__date_time_manager.index_of_week_day(week_day_name) == 5 or
                self.__date_time_manager.index_of_week_day(week_day_name) == 6)



