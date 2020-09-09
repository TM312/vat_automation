from .model import Category
from .schema import category_dto


BASE_ROUTE = "category"


def attach_category(api, app):
    from .controller import ns as category_ns
    api.add_namespace(category_ns, path=f"/{BASE_ROUTE}")
