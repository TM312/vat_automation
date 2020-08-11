from .model_parent import Business
from .schema_parent import business_sub_dto, business_dto, business_admin_dto

BASE_ROUTE = "business"


def attach_business(api, app):
    from .controller_parent import ns as business_ns
    from .seller_firm.controller import ns as seller_firm_ns
    from .accounting_firm.controller import ns as accounting_firm_ns
    from .customer_firm.controller import ns as customer_firm_ns

    api.add_namespace(business_ns, path=f"/{BASE_ROUTE}")
    api.add_namespace(seller_firm_ns, path=f"/{BASE_ROUTE}/seller_firm")
    api.add_namespace(accounting_firm_ns, path=f"/{BASE_ROUTE}/accounting_firm")
    api.add_namespace(customer_firm_ns, path=f"/{BASE_ROUTE}/customer_firm")
