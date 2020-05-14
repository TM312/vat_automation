from typing import List

from flask import request
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from .schema import accounting_firm_dto
from .service import AccountingFirmService
from .model import AccountingFirm
from .interface import AccountingFirmInterface

from ...auth import TokenInterface
from ...utils import login_required, accepted_u_types, confirmation_required


ns = Namespace("AccountingFirm", description="Accounting Firm Related Operations")  # noqa
ns.add_model(accounting_firm_dto.name, accounting_firm_dto)


@ns.route("/")
class AccountingFirmResource(Resource):
    @login_required
    @ns.marshal_with(accounting_firm_dto)
    def get(self) -> AccountingFirm:
        """Get own Accounting Firm"""
        tax_auditor = g.user
        return AccountingFirmService.get_own(tax_auditor)

    @ns.expect(accounting_firm_dto, validate=True)
    def post(self):
        """Create A Single Accounting Firm"""
        accounting_firm_data: AccountingFirmInterface = request.json
        return AccountingFirmService.create_accounting_firm(accounting_firm_data)

    @login_required
    def delete(self) -> Response:
        """Delete A Single Accounting Business"""
        tax_auditor = g.user
        return AccountingFirmService.delete_own(tax_auditor)

    @login_required
    @ns.expect(accounting_firm_dto, validate=True)
    @ns.marshal_with(accounting_firm_dto)
    #@accepted_u_types('admin', 'tax_auditor')
    def put(self) -> AccountingFirm:
        """Update A own accounting firm"""
        tax_auditor = g.user
        data_changes: AccountingFirmInterface = request.json  # JSON body of a request
        return AccountingFirmService.update_own(tax_auditor, data_changes)



@ns.route("/clients")
class AccountingFirmClientListResource(Resource):
    """Get all Company Clients"""
    @login_required
    @accepted_u_types('admin', 'tax_auditor')
    #@confirmation_required
    @ns.marshal_list_with(accounting_firm_dto, envelope='data')
    def get(self) -> List[AccountingFirm]:
        """List Of Registered Accountings"""
        tax_auditor = g.user
        return AccountingFirmService.get_own_clients(tax_auditor)
