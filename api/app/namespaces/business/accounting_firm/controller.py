from typing import List

from flask import request
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from .schema import accounting_firm_dto
from .service import AccountingFirmService
from .model import AccountingFirm
from .interface import AccountingFirmInterface

from ...utils.decorators import login_required, accepted_u_types, confirmation_required


ns = Namespace("AccountingFirm", description="Accounting Firm Related Operations")  # noqa
ns.add_model(accounting_firm_dto.name, accounting_firm_dto)


@ns.route('/')
class AccountingFirmResource(Resource):
    '''Get all Accounting Firms'''
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_list_with(accounting_firm_dto, envelope='data')
    def get(self) -> List[AccountingFirm]:
        '''List Of Registered AccountingFirm Firms'''
        return AccountingFirmService.get_all()

    @ns.expect(accounting_firm_dto, validate=True)
    @ns.marshal_with(accounting_firm_dto)
    def post(self):
        """Create A Single Seller Firm"""
        accounting_firm_data: AccountingFirmInterface = request.json
        return AccountingFirmService.create(accounting_firm_data)


@ns.route('/<int:accounting_firm_id>')
@ns.param('accounting_firm_id', 'Seller firm ID')
class AccountingFirmIdResource(Resource):
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_with(accounting_firm_dto)
    def get(self, accounting_firm_id: int) -> AccountingFirm:
        '''Get One AccountingFirm'''
        return AccountingFirmService.get_by_id(accounting_firm_id)

    @login_required
    @accepted_u_types('admin')
    def delete(self, accounting_firm_id: int) -> Response:
        '''Delete A Single AccountingFirm'''
        return AccountingFirmService.delete_by_id(accounting_firm_id)




@ns.route("/clients")
class AccountingFirmClientListResource(Resource):
    """Get all Company Clients"""
    @login_required
    @accepted_u_types('admin', 'tax_auditor')
    #@confirmation_required
    @ns.marshal_list_with(accounting_firm_dto, envelope='data')
    def get(self) -> List[AccountingFirm]:
        """List Of Registered Accountings"""
        return AccountingFirmService.get_own_clients(tax_auditor=g.user)
