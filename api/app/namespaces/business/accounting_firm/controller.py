from typing import List

from flask import request
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from . import AccountingFirm
from . import accounting_firm_dto, accounting_firm_sub_dto
from .service import AccountingFirmService
from .interface import AccountingFirmInterface

from ...utils.decorators import login_required, accepted_u_types, confirmation_required


ns = Namespace("AccountingFirm", description="Accounting Firm Related Operations")  # noqa
ns.add_model(accounting_firm_sub_dto.name, accounting_firm_sub_dto)
ns.add_model(accounting_firm_dto.name, accounting_firm_dto)


@ns.route('/')
class AccountingFirmResource(Resource):
    '''Get all Accounting Firms'''
    # @login_required
    # @accepted_u_types('admin')
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


@ns.route('/<string:accounting_firm_public_id>')
@ns.param('accounting_firm_public_id', 'Seller firm ID')
class AccountingFirmIdResource(Resource):
    # @login_required
    # @accepted_u_types('admin')
    @ns.marshal_with(accounting_firm_dto, envelope='data')
    def get(self, accounting_firm_public_id: str) -> AccountingFirm:
        '''Get One AccountingFirm'''
        return AccountingFirmService.get_by_public_id(accounting_firm_public_id)

    # @login_required
    # @accepted_u_types('admin')
    def delete(self, accounting_firm_public_id: int) -> Response:
        '''Delete A Single AccountingFirm'''
        return AccountingFirmService.delete_by_public_id(accounting_firm_public_id)
