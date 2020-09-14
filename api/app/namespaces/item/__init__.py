from .model import Item, ItemHistory
from .schema import item_dto, item_sub_dto, item_admin_dto, item_history_dto


BASE_ROUTE = "item"


def attach_item(api, app):
    from .controller import ns as item_ns
    api.add_namespace(item_ns, path=f"/{BASE_ROUTE}")
