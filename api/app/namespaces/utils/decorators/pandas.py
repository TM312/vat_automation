import pandas as pd
from flask import request, g

from werkzeug.exceptions import UnsupportedMediaType


def none_if_not_column(f):
    def wrap(*args, **kwargs):
        if kwargs.get('column') in df.columns:
            return f(*args, **kwargs)
        else:
            return None

    return wrap


def allow_none_column(f):
    def wrap(*args, **kwargs):
        df = args[0]
        i = args[1]
        column = kwargs.get('column')
        if pd.isnull(df.iloc[i][column]):
            return f(*args, **kwargs)
        else:
            return None

    return wrap
