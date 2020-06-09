from mypy_extensions import TypedDict

class ChannelInterface(TypedDict, total=False):
    code: str
    name: str
    platform_code: str
    description: str
