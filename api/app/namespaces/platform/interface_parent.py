
from mypy_extensions import TypedDict
from datetime import date
from typing import List


class PlatformInterface(TypedDict, total=False):
    code: str
    name: str
    channels: List['app.namespaces.channel.Channel']
