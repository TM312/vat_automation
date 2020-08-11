from .model import Tag
from .schema import tag_dto


BASE_ROUTE = "tag"

def attach_tag(api, app):
    from .controller import ns as tag_ns
    api.add_namespace(tag_ns, path=f"/{BASE_ROUTE}")
