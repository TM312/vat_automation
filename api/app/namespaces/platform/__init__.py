from .model_parent import Platform
from .schema_parent import platform_dto


BASE_ROUTE = "platform"


def attach_platform(api, app):

    from .controller import ns as platform_ns
    from .amazon.controller import ns as amazon_ns

    api.add_namespace(platform_ns, path=f"/{BASE_ROUTE}")
    api.add_namespace(amazon_ns, path=f"/{BASE_ROUTE}/amazon")
