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
        # print('*args: ->', *args, flush=True)
#         print('*kwargs: ->', **kwargs, flush=True)
        df = args[0]
        i = args[1]
        print('i: {}'.format(i), flush=True)
        column = kwargs.get('column')
        print('column: {}'.format(column), flush=True)
        if pd.isnull(df.iloc[i][column]):
            return None
        else:
            return f(*args, **kwargs)

    return wrap
