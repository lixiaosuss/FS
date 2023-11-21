import time
import datetime
from time import strftime


def timestamp():
    """时间戳"""
    return time.time()


def datetime_strftime(fmt="%Y%m"):
    """datetime格式化时间"""
    return datetime.datetime.now().strftime(fmt)


def sleep(seconds=1.0):
    """
    睡眠时间
    """
    time.sleep(seconds)


now_time = strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    print(datetime_strftime())
