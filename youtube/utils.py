# utils.py

import isodate



def convert_isodate_to_seconds(duration):
    return isodate.parse_duration(duration).total_seconds()


