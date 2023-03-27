import operator
import os
from collections.abc import Iterable
from functools import reduce

from dotenv import load_dotenv


def clean_keys(items: dict | list):
    """Removes the xml formatting from the dict keys"""
    if type(items) is dict:
        bad_keys = [
            key for key in items.keys()
            if key and len(key) > 0 and key[0] in ["@", "#"]
        ]

        for bad_key in bad_keys:
            good_key = bad_key[1:]
            items[good_key] = items.pop(bad_key)

        [
            clean_keys(value)
            for value in items.values()
            if type(value) in [list, dict]
        ]
    elif type(items) is list:
        [
            clean_keys(item)
            for item in items
            if type(item) in [dict, list]
        ]


def coord_to_float(coord: str) -> float:
    """Converts a coordinate with a compass direction to a float"""
    if coord[-1] in ['W', 'S']:
        return -float(coord[:-1])
    else:
        return float(coord[:-1])


def get_nested_val(
        ddict: dict[str, any],
        keys: Iterable[str]
):
    return reduce(operator.getitem, keys, ddict)


load_dotenv()

POST_HOST = os.getenv("POST_HOST")
POST_PORT = os.getenv("POST_PORT")

POST_URL = f"{POST_HOST}:{POST_PORT}/weather/post"

