from mypy_extensions import TypedDict
from typing import List


class PlatformInterface(TypedDict, total=False):
    code: str
    name: str
