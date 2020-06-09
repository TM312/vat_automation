from .model_parent import User, Action
from .schema_parent import user_dto, user_dto_admin


BASE_ROUTE = "user"

def attach_user(api, app):
    from .admin.controller import ns as admin_ns
    from .seller.controller import ns as seller_ns
    from .tax_auditor.controller import ns as tax_auditor_ns

    api.add_namespace(admin_ns, path=f"/{BASE_ROUTE}/admin")
    api.add_namespace(seller_ns, path=f"/{BASE_ROUTE}/seller")
    api.add_namespace(tax_auditor_ns, path=f"/{BASE_ROUTE}/tax_auditor")
