from . import DefinedSegment


def date_day() -> DefinedSegment:
    """
    The current day of the week.
    """
    import datetime
    current_date = datetime.datetime.now()
    return current_date.strftime("%A")


def date(format="%Y-%m-%d") -> DefinedSegment:
    """
    The current date.

    Parameters:
    -----------
    `format` (str):
        The format of the date. Defaults to "%Y-%m-%d".
    """
    import datetime
    current_date = datetime.datetime.now()
    return current_date.strftime(format)


def time(format="%H:%M") -> DefinedSegment:
    """
    The current time.

    Parameters:
    -----------
    `format` (str): 
        The format of the time. Defaults to "%H:%M".
    """
    import datetime
    current_date = datetime.datetime.now()
    return current_date.strftime(format)
