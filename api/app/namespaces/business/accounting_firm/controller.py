from typing import List

from flask import request
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource


from app.extensions import mail
from .schema import accounting_firm_dto
from .service import Accounting_FirmService
from .model import Accounting_Firm
from .interface import Accounting_FirmInterface
from ..auth.interface import TokenInterface

from ..utils.decorators.auth import login_required, accepted_roles, confirmation_required


ns = Namespace("Accounting_Firm", description="Accounting Firm Related Operations")  # noqa
ns.add_model(accounting_firm_dto.name, accounting_firm_dto)


@ns.route("/")
class AdminAccountingListResource(Resource):
    """Get all Accounting Firms"""
    @login_required
    @accepted_roles('admin')
    #@confirmation_required
    @ns.marshal_list_with(accounting_dto, envelope='data')
    def get(self) -> List[Accounting]:
        """List Of Registered Accounting Businesses"""
        return AccountingService.get_all()

    @ns.expect(accounting_dto, validate=True)
    def post(self):
        """Create A Single Accounting"""
        accounting_data: AccountingInterface = request.json
        return AccountingService.create_accounting_business(accounting_data)


@ns.route("/<string:public_id>")
@ns.param("public_id", "Public accounting ID")
class AdminAccountingIdResource(Resource):
    @login_required
    @accepted_roles('admin')
    @ns.marshal_with(accounting_dto)
    def get(self, public_id: str) -> Accounting:
        """Get One Accounting"""
        return AccountingService.get_by_id(public_id)

    @login_required
    @accepted_roles('admin')
    def delete(self, public_id: str) -> Response:
        """Delete A Single Accounting Business"""
        return AccountingService.delete_by_id(public_id)

    @login_required
    @accepted_roles('admin', 'tax_auditor')
    @ns.expect(accounting_dto, validate=True)
    @ns.marshal_with(accounting_dto)
    def put(self, public_id: str) -> Accounting:
        """Update A Accounting Business' Details"""
        data_changes: AccountingInterface = request.json  # JSON body of a request
        return AccountingService.update(public_id, data_changes)


@ns.route("/<string:public_id>/clients")
class AccountingFirmClientListResource(Resource):
    """Get all Company Clients"""
    @login_required
    @accepted_roles('admin', 'tax_auditor')
    #@confirmation_required
    @ns.marshal_list_with(accounting_dto, envelope='data')
    def get(self) -> List[Accounting]:
        """List Of Registered Accountings"""
        return AccountingService.get_all_clients(public_id)

    @login_required
    @accepted_roles('admin', 'tax_auditor')
    @ns.expect(seller_dto, validate=True)
    def post(self):
        """Create A Client"""
        client_data: AccountingInterface = request.json
        user = g.user
        return SellerService.create_unclaimed_seller(user, client_data)
