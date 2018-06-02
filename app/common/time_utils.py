__author__ = 'chenfeiyu'


class TimeUtils():
    @staticmethod
    def get_dd_mm_yyyy(date):
        if date is not None:
            return date.strftime("%d-%m-%Y")
        else:
            return None

    @staticmethod
    def get_yyyy_mm_dd(date):
        if date is not None:
            return date.strftime("%Y-%m-%d")
        else:
            return None