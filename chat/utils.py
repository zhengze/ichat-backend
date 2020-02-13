import time
import datetime


def datetime_format(record_time):
    now = datetime.datetime.now()
    deltaH = datetime.timedelta(seconds=86400)

    if now - record_time < deltaH:
        return ":".join([str(record_time.hour), str(record_time.second)])
    else:
        return "".join([str(record_time.month), "月",
                        str(record_time.day), "日"])


def datetime2timestamp(record_time):
    return int(time.mktime(record_time.timetuple()))
