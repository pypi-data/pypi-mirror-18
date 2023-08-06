import datetime

COMMON_DATE_FORMAT = "%Y-%m-%d"
COMMON_DATETIME_FORMAT = "{date_fmt} %H:%M:%S".format(
    date_fmt=COMMON_DATE_FORMAT)
SIMPLE_DATETIME_FORMAT = "%m-%d %H:%M"


def common_fmt_dt(dt):
    """按常规格式获取datetime对象的字符串表示
    """
    return dt.strftime(COMMON_DATETIME_FORMAT)


def simple_fmt_dt(dt):
    """简单版的datetime对象字符串表示
    """
    return dt.strftime(SIMPLE_DATETIME_FORMAT)


def get_timedelta_desc(dt):
    time_delta = datetime.datetime.now() - dt
    delta_seconds = int(time_delta.total_seconds())
    if delta_seconds < 60:
        return "{} 秒".format(delta_seconds)
    elif delta_seconds < 3600:
        return "{} 分".format(int(delta_seconds / 60))
    elif delta_seconds < 24 * 3600:
        hours = int(delta_seconds / 3600)
        minutes = int((delta_seconds % 3600) / 60)

        if minutes:
            return "{0} 小时 {1} 分钟".format(hours, minutes)
        else:
            return "{0} 小时".format(hours)
    else:
        days = int(delta_seconds / 3600 / 24)
        hours = (delta_seconds % (3600 * 24)) / 3600

        if hours:
            return "{0} 天 {1} 小时".format(days, int(hours))
        else:
            return "{0} 天".format(days)


def is_current_year(year):
    """判断一个年份是否是当前年份
    """
    now = datetime.datetime.now()
    return now.year == year


def is_current_month(month):
    """判断一个月份是否是当前月份
    """
    now = datetime.datetime.now()
    return now.month == month


def is_current_day(day):
    """判断一个日期是否是当前日期
    """
    now = datetime.datetime.now()
    return now.day == day


def current_year():
    """获取当前年份，通常用于页面footer
    """
    return datetime.datetime.now().year
