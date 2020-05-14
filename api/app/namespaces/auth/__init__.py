from .model import Token  # noqa
from .schema import auth_dto  # noqa
from .service import TokenService
from .interface import TokenInterface

BASE_ROUTE = "auth"

#def attach_auth(api, app, root):
def attach_auth(api, app):
    from .controller import ns as auth_ns

    #api.add_namespace(auth_ns, path=f"/{root}/{BASE_ROUTE}")
    api.add_namespace(auth_ns, path=f"/{BASE_ROUTE}")
