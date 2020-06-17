from .model import Platform
from .schema import platform_dto


BASE_ROUTE = "platform"


def attach_platform(api, app):

    from .controller import ns as platform_ns
    api.add_namespace(platform_ns, path=f"/{BASE_ROUTE}")
