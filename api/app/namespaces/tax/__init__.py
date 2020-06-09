

BASE_ROUTE = "tax"


def attach_tax(api, app):
    from .tax_code.controller import ns as tax_code_ns
    from .tax_treatment.controller import ns as tax_treatment_ns
    from .vat.controller import ns as vat_ns
    from .vatin.controller import ns as vatin_ns

    api.add_namespace(tax_code_ns, path=f"/{BASE_ROUTE}/tax_code")
    api.add_namespace(tax_treatment_ns, path=f"/{BASE_ROUTE}/tax_treatment")
    api.add_namespace(vat_ns, path=f"/{BASE_ROUTE}/vat")
    api.add_namespace(vatin_ns, path=f"/{BASE_ROUTE}/vatin")
