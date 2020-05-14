from .vatin.model import VATIN
from .vatin.service import VATINService

from .tax_code.model import TaxCode

from .tax_rate.model import TaxRate, TaxRateType

from .tax_treatment.model import TaxTreatment

BASE_ROUTE = "model"

def attach_business(api, app):
    from .vies.controller import ns as vies_ns

    api.add_namespace(accounting_firm_ns, path=f"/{BASE_ROUTE}/vies")
