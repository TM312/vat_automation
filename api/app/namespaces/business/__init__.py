BASE_ROUTE = "business"

# def attach_auth(api, app, root):


def attach_business(api, app):
    from .seller_firm.controller import ns as seller_firm_ns
    from .accounting_firm.controller import ns as accounting_firm_ns

    api.add_namespace(accounting_firm_ns, path=f"/{BASE_ROUTE}/seller_firm")
    api.add_namespace(accounting_firm_ns, path=f"/{BASE_ROUTE}/accounting_firm")
