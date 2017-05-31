# Sources:
# http://evaisse.com/post/93417709/python-pretty-date-function
# https://stackoverflow.com/questions/1551382

from datetime import datetime

def prettify_date(time = False):
    """
    Get a datetime object or an int() Unix timestamp and return a
    pretty string like 'An hour ago', 'Yesterday', '3 months ago',
    'Just now', etc.
    """
    
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = 0
    diff_sec = diff.seconds
    diff_day = diff.days

    if diff_day < 0:
        return ""

    if diff_day == 0:
        if diff_sec < 10:
            return "Just now"
        if diff_sec < 60:
            return str(diff_sec) + " seconds ago"
        if diff_sec < 120:
            return "A minute ago"
        if diff_sec < 3600:
            return str(diff_sec / 60) + " minutes ago"
        if diff_sec < 7200:
            return "An hour ago"
        if diff_sec < 86400:
            return str(diff_sec / 3600) + " hours ago"
    if diff_day == 1:
        return "Yesterday"
    if diff_day < 7:
        return str(diff_day) + " days ago"
    if diff_day < 31:
        return str(diff_day / 7) + " weeks ago"
    if diff_day < 365:
        return str(diff_day / 30) + " months ago"
    return str(diff_day / 365) + " years ago"
