from .admin.model import Admin

from .seller.model import Seller
from .seller.service import SellerService
from .seller.interface import SellerInterface
from .seller.schema import seller_dto, seller_dto_admin

from .tax_auditor.model import TaxAuditor
from .tax_auditor.service import TaxAuditorService
from .tax_auditor.interface import !!!
from .tax_auditor.schema import tax_auditor_dto, tax_auditor_dto_admin

from .model_parent import User, Action
from .service_parent import UserService
from .schema_parent import user_dto, user_dto_admin, action_dto

BASE_ROUTE = "user"

#def attach_auth(api, app, root):
def attach_user(api, app):
    from .seller.controller import ns as seller_ns
    from .tax_auditor.controller import ns as tax_auditor_ns
    from .controller_parent import ns as user_ns


    api.add_namespace(seller_ns, path=f"/{BASE_ROUTE}/seller")
    api.add_namespace(tax_auditor_ns, path=f"/{BASE_ROUTE}/tax_auditor")
    api.add_namespace(user_ns, path=f"/{BASE_ROUTE}")
