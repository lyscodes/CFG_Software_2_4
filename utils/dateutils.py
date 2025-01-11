from datetime import datetime, timezone

def get_utc_date():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d')


def get_month_name(date_object):
    month_dt = str(date_object.month)
    month_object = datetime.strptime(month_dt, "%m")
    return month_object.strftime("%B")
