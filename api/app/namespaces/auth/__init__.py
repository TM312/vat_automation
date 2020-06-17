from .model import Token
from .schema import auth_dto

BASE_ROUTE = "auth"

#def attach_auth(api, app, root):
def attach_auth(api, app):
    from .controller import ns as auth_ns
    api.add_namespace(auth_ns, path=f"/{BASE_ROUTE}")
