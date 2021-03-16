from datetime import datetime
import datetime as dt
from dateutil import tz
from .settings import USE_TZ, TIME_ZONE


def datetime_now() -> datetime:
    if USE_TZ:
        now = datetime.now(tz.gettz(TIME_ZONE))
    else:
        now = datetime.now()

    return now


def datetime_in_x_days(days=0, date=None) -> datetime:
    if date is None:
        date = datetime_now()
    return date + dt.timedelta(days=days)


def formatted_date(date):
    return date.isoformat()[:-6] + 'Z'
