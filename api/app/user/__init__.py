from .model import User  # noqa
from .schema import user_dto  # noqa

BASE_ROUTE = "user"


def attach_user(api, app, root):
    from .controller import ns as user_ns

    api.add_namespace(user_ns, path=f"{root}/{BASE_ROUTE}")
