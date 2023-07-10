# utils.py

import numpy as np

import isodate
from typing import Union



def convert_isodate_to_seconds(duration : str) -> int:
    r"""
    Convert the ISO 8601 `duration` string into seconds (int).
    """
    return int(isodate.parse_duration(duration).total_seconds())



def get_value_from_key(d : dict, key : Union[str,list[str]], fill_value : object = np.NaN) -> object:
    r"""
    Get the value from the dictionary `d` with the associated `key`. If
    the key is missing from the dictionary, then use the `fill_value`.
    """

    try:
        if isinstance(key, str):
            value = d[key]
        # if `key` is a list, then recursively exhaust the list of keys
        elif isinstance(key, list):
            if len(key) == 0:
                raise ValueError("Value for `key` cannot be empty list.")
            elif len(key) == 1:
                value = d[key[0]]
            else:
                value = get_value_from_key(d[key[0]], key[1:])
    except KeyError:
        # pass error silently
        value = fill_value
    
    return value


