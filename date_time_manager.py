from datetime import datetime, timedelta


class DateTimeManager:
    def __init__(self):
        self.__days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.__month_dict = {
            'January': 0, 'February': 1, 'March': 2, 'April': 3,
            'May': 4, 'June': 5, 'July': 6, 'August': 7,
            'September': 8, 'October': 9, 'November': 10, 'December': 11
        }

    def find_weekdays(self, year, month, day_of_week):
        # Convert the day_of_week to a weekday number (0=Monday, 6=Sunday)
        weekday = self.__days.index(day_of_week.title())

        # Start at the beginning of the month
        date = datetime(year, month, 1)

        # Move to the first occurrence of the desired weekday
        while date.weekday() != weekday:
            date += timedelta(days=1)

        # Collect all occurrences of the weekday in the month
        dates = []
        while date.month == month:
            dates.append(date.strftime('%Y-%m-%d'))
            date += timedelta(days=7)  # Move to the next week
        return dates

    def month_name_to_index(self, month_name):
        month_index = self.__month_dict.get(month_name.title())
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
