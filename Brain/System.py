import datetime
import pytz


class System:

    def __init__(self):
        self.__DATE_TIME_REFERENCE = pytz.utc
        self.__TIME_SEPARATOR = ":"
        self.__DATE_SEPARATOR = " "
        self.__TIME_FORMAT = f"%H{self.__TIME_SEPARATOR}%M"
        self.__DATE_FORMAT = f"%A{self.__DATE_SEPARATOR}%d{self.__DATE_SEPARATOR}%B{self.__DATE_SEPARATOR}%Y"
        self.__DATE_TIME_FORMAT = f"{self.__DATE_FORMAT} {self.__TIME_FORMAT}"

    def get_time(self):
        return datetime.datetime.now(self.__DATE_TIME_REFERENCE).astimezone().strftime(self.__TIME_FORMAT).split(
            self.__TIME_SEPARATOR)

    def get_time_specific_region(self, region: str):
        try:
            return datetime.datetime.now(pytz.timezone(f"Africa/{region}")).strftime(self.__TIME_FORMAT).split(
                self.__TIME_SEPARATOR)
        except pytz.exceptions.UnknownTimeZoneError:
            try:
                return datetime.datetime.now(pytz.timezone(f"Europe/{region}")).strftime(self.__TIME_FORMAT).split(
                    self.__TIME_SEPARATOR)
            except pytz.exceptions.UnknownTimeZoneError:
                try:
                    return datetime.datetime.now(pytz.timezone(f"Asia/{region}")).strftime(self.__TIME_FORMAT).split(
                        self.__TIME_SEPARATOR)
                except pytz.exceptions.UnknownTimeZoneError:
                    try:
                        return datetime.datetime.now(pytz.timezone(f"America/{region}")).strftime(
                            self.__TIME_FORMAT).split(
                            self.__TIME_SEPARATOR)
                    except pytz.exceptions.UnknownTimeZoneError:
                        try:
                            return datetime.datetime.now(pytz.timezone(f"Australia/{region}")).strftime(
                                self.__TIME_FORMAT).split(
                                self.__TIME_SEPARATOR)
                        except pytz.exceptions.UnknownTimeZoneError:
                            return ["00", "00", "00"]

    def get_date(self):
        return datetime.datetime.now(self.__DATE_TIME_REFERENCE).astimezone().strftime(self.__DATE_FORMAT).split(
            self.__DATE_SEPARATOR)

    def __make_date_readable(self, ):
        pass

    def get_date_time(self):
        return datetime.datetime.now(self.__DATE_TIME_REFERENCE).astimezone().strftime(self.__DATE_TIME_FORMAT)
