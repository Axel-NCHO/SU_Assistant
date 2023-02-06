import datetime
import pytz


class System:

    def __init__(self):
        self.__date_time_reference = pytz.utc

    def get_time(self):
        return datetime.datetime.now(self.__date_time_reference).strftime("%H:%M").split(":")

    def get_date(self):
        return datetime.datetime.now(self.__date_time_reference).strftime("%Y-%m-%d").split(":")

    def get_date_time(self):
        return datetime.datetime.now(self.__date_time_reference).strftime("%Y-%m-%d %H:%M:%S")
