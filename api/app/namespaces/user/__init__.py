from .model import User  # noqa
from .schema import user_dto  # noqa

BASE_ROUTE = "user"

#def attach_auth(api, app, root):
def attach_user(api, app):
    from .seller.controller import ns as seller_ns
    from .tax_auditor.controller import ns as tax_auditor_ns
    from .controller_parent import ns as user_ns


    api.add_namespace(seller_ns, path=f"/{BASE_ROUTE}/seller")
    api.add_namespace(tax_auditor_ns, path=f"/{BASE_ROUTE}/tax_auditor")
    api.add_namespace(user_ns, path=f"/{BASE_ROUTE}")
