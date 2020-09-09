from .model import UserTag
from .schema import user_tag_dto


BASE_ROUTE = "user_tag"

def attach_user_tag(api, app):
    from .controller import ns as user_tag_ns
    api.add_namespace(user_tag_ns, path=f"/{BASE_ROUTE}")
