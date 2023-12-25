from datetime import datetime, timedelta
from difflib import SequenceMatcher


class DateTimeManager:
    def __init__(self):
        self.__days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.__month_dict = {
            'January': 0, 'February': 1, 'March': 2, 'April': 3,
            'May': 4, 'June': 5, 'July': 6, 'August': 7,
            'September': 8, 'October': 9, 'November': 10, 'December': 11
        }

    def refine_day_name(self, week_day_name):
        day_name = week_day_name
        if week_day_name[-1] == 's':
            day_name = week_day_name[:-1]
        biggest_similarity_index = 0
        biggest_similarity = -1
        for name_index, name in enumerate(self.__days):
            similarity = SequenceMatcher(None, day_name, name).ratio()
            if similarity > biggest_similarity:
                biggest_similarity_index = name_index
                biggest_similarity = similarity
        return self.__days[biggest_similarity_index]





    def find_weekdays(self, year, month, day_of_week):
        day_name = day_of_week
        if day_name[-1] == 's':
            day_name = day_of_week[:-1]
        # Convert the day_of_week to a weekday number (0=Monday, 6=Sunday)
        weekday = self.__days.index(day_name.title())

        # Start at the beginning of the month
        tmp_date = datetime(int(year), int(month), 1)

        # Move to the first occurrence of the desired weekday
        while tmp_date.weekday() != weekday:
            tmp_date += timedelta(days=1)

        # Collect all occurrences of the weekday in the month
        tmp_dates = []
        while tmp_date.month == month:
            tmp_dates.append(tmp_date.strftime('%Y-%m-%d'))
            tmp_date += timedelta(days=7)  # Move to the next week
        return tmp_dates

    def month_name_to_index(self, month_name):
        month_index = self.__month_dict.get(month_name.title())+1 #months index is starting from 0, but month number is from 1
        if month_index is not None:
            return month_index
        else:
            raise ValueError(f"'{month_name}' is not a valid month name.")

    def index_of_week_day(self, week_day_name):
        try:
            # Use the index() method to find the first occurrence of the item
            index_position = self.__days.index(week_day_name)
            return index_position
        except ValueError:
            # If the item is not found, a ValueError is raised
            return f"The item '{week_day_name}' was not found in the list."


if __name__ == "__main__":
    # Usage: find_weekdays(2023, 12, 'Monday') for all Mondays in December 2023
    year = 2022  # Change to the desired year
    month = 12  # Change to the desired month (1-12)
    day_of_week = 'Thursday'  # Change to the desired weekday ('Monday', 'Tuesday', etc.)

    date_time_manager = DateTimeManager()

    dates = date_time_manager.find_weekdays(year, month, day_of_week)

    for date in dates:
        print(date)

    month_name = "March"  # Replace with the month name you want to convert
    index = date_time_manager.month_name_to_index(month_name)
    print(f"The index of {month_name} is {index}.")
