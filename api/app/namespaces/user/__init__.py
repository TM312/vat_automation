from .model_parent import User, Action
from .schema_parent import user_dto, user_dto_admin, user_sub_dto, action_dto

BASE_ROUTE = "user"

def attach_user(api, app):
    from .controller_parent import ns as user_ns
    from .admin.controller import ns as admin_ns
    from .seller.controller import ns as seller_ns
    from .tax_auditor.controller import ns as tax_auditor_ns
    from .subscriber.controller import ns as subscriber_ns

    api.add_namespace(user_ns, path=f"/{BASE_ROUTE}")
    api.add_namespace(admin_ns, path=f"/{BASE_ROUTE}/admin")
    api.add_namespace(seller_ns, path=f"/{BASE_ROUTE}/seller")
    api.add_namespace(tax_auditor_ns, path=f"/{BASE_ROUTE}/tax_auditor")
    api.add_namespace(subscriber_ns, path=f"/{BASE_ROUTE}/subscriber")
