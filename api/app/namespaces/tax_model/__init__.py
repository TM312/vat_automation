BASE_ROUTE = "model"

def attach_business(api, app):
    from .vies.controller import ns as vies_ns

    api.add_namespace(accounting_firm_ns, path=f"/{BASE_ROUTE}/vies")
