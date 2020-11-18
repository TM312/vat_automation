from .model import Channel
from .schema import channel_dto, channel_sub_dto


BASE_ROUTE = "channel"

#def attach_channel(api, app, root):
def attach_channel(api, app):
    from .controller import ns as channel_ns
    api.add_namespace(channel_ns, path=f"/{BASE_ROUTE}")
