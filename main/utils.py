from datetime import datetime
from dateutil import tz
from .settings import USE_TZ, TIME_ZONE


def datetime_now() -> datetime:
    if USE_TZ:
        now = datetime.now(tz.gettz(TIME_ZONE))
    else:
        now = datetime.now()

    return now


def formatted_date(date):
    return date.isoformat()[:-6] + 'Z'
