from django.utils import timezone
import datetime


class Utils:
    @staticmethod
    def get_date():
        date = datetime.date.today()
        return date

    @staticmethod
    def get_date_time():
        return timezone.now()