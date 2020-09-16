from .model import ItemTag
from .schema import item_tag_dto


BASE_ROUTE = "item_tag"

def attach_item_tag(api, app):
    from .controller import ns as item_tag_ns
    api.add_namespace(item_tag_ns, path=f"/{BASE_ROUTE}")
