class PeakData:
    def __init__(self, peak_hour, peak_period, peak_hour_max_quarter, peak_period_max_quarter):
        self.peak_hour = peak_hour
        self.peak_hour_max_quarter = peak_hour_max_quarter
        self.peak_period = peak_period
        self.peak_period_max_quarter = peak_period_max_quarter


class AverageTravelTimeData:
    def __init__(self, peak_hour_average_travel_time, peak_period_average_travel_time,
                 peak_hour_mphf, peak_period_mphf):
        self.peak_hour_average_travel_time = peak_hour_average_travel_time
        self.peak_hour_mphf = peak_hour_mphf
        self.peak_period_average_travel_time = peak_period_average_travel_time
        self.peak_period_mphf = peak_period_mphf


class ExcelRow:
    def __init__(self, link_id, day, month, year, is_weekday,
                 is_public_holidays, is_school_terms, peak_hour,
                 peak_period, peak_hour_max_quarter, peak_period_max_quarter,
                 peak_hour_average_travel_time, peak_period_average_travel_time,
                 peak_hour_mphf, peak_period_mphf, peak_day_time,
                 peak_hour_seasonality, peak_period_seasonality,
                 local_board, area, direction):
        self.link_id = link_id
        self.day = day
        self.month = month
        self.year = year
        self.is_weekday = is_weekday
        self.is_public_holidays = is_public_holidays
        self.is_school_terms = is_school_terms
        self.peak_hour = peak_hour
        self.peak_period = peak_period
        self.peak_hour_max_quarter = peak_hour_max_quarter
        self.peak_period_max_quarter = peak_period_max_quarter
        self.peak_hour_average_travel_time = peak_hour_average_travel_time
        self.peak_period_average_travel_time = peak_period_average_travel_time
        self.peak_hour_mphf = peak_hour_mphf
        self.peak_period_mphf = peak_period_mphf
        self.peak_day_time = peak_day_time
        self.peak_hour_seasonality = peak_hour_seasonality
        self.peak_period_seasonality = peak_period_seasonality
        self.local_board = local_board
        self.area = area
        self.direction = direction




