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

    def __init_holidays(self):
        self.__public_holidays_dict = {
            'Christmas Day 2022': pd.to_datetime('2022-12-25'),
            'Boxing Day 2022': pd.to_datetime('2022-12-26'),
            'New Year\'s Day 2023': pd.to_datetime('2023-01-01'),
            'Day after New Year\'s Day 2023': pd.to_datetime('2023-01-02'),
            'Auckland Anniversary 2023': pd.to_datetime('2023-01-30'),
            'Waitangi Day 2023': pd.to_datetime('2023-02-06'),
            'Good Friday 2023': pd.to_datetime('2023-04-07'),
            'Easter Monday 2023': pd.to_datetime('2023-04-10'),
            'ANZAC Day 2023': pd.to_datetime('2023-04-25'),
            'King\'s Birthday 2023': pd.to_datetime('2023-06-05'),
            'Labour Day 2023': pd.to_datetime('2023-10-23'),
            'Christmas Day 2023': pd.to_datetime('2023-12-25'),
            'Boxing Day 2023': pd.to_datetime('2023-12-26'),
        }

        self.__school_holidays_dict = {
            'Term 4, 2022': (pd.to_datetime('2022-12-21'), pd.to_datetime('2022-12-31')), # december
            'Summer Holidays 2022-2023': (pd.to_datetime('2022-12-21'), pd.to_datetime('2023-02-01')), #december - anuary - february wednsday
            'Term 1, 2023': (pd.to_datetime('2023-02-01'), pd.to_datetime('2023-04-15')),
            'Autumn Holidays 2023': (pd.to_datetime('2023-04-15'), pd.to_datetime('2023-04-30')),
            'Term 2, 2023': (pd.to_datetime('2023-04-30'), pd.to_datetime('2023-07-15')),
            'Winter Holidays 2023': (pd.to_datetime('2023-07-15'), pd.to_datetime('2023-07-31')),
            'Term 3, 2023': (pd.to_datetime('2023-07-31'), pd.to_datetime('2023-10-15')),
            'Spring Holidays 2023': (pd.to_datetime('2023-10-15'), pd.to_datetime('2023-10-31')),
            'Term 4, 2023': (pd.to_datetime('2023-10-31'), pd.to_datetime('2023-12-31')),
        }
    def __is_public_holiday(self, date):
        for holiday_date in self.__public_holidays_dict.values():
            #print("date:", date.date(), " holiday date:", holiday_date.date(), " status:", date.date() == holiday_date.date())
            if date.date() == holiday_date.date():
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

    # Function to check if a date is a school holiday
    def __is_school_holiday(self, date):
        for start_date, end_date in self.__school_holidays_dict.values():
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



