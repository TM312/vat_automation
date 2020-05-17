
BASE_ROUTE = "business"


def attach_business(api, app):
    from .seller_firm.controller import ns as seller_firm_ns
    from .accounting_firm.controller import ns as accounting_firm_ns
    #from .controller_parent import ns as business_ns

    api.add_namespace(accounting_firm_ns, path=f"/{BASE_ROUTE}/seller_firm")
    api.add_namespace(accounting_firm_ns, path=f"/{BASE_ROUTE}/accounting_firm")
    #api.add_namespace(user_ns, path=f"/{BASE_ROUTE}")
