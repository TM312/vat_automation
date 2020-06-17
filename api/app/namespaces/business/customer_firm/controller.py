from typing import List

from flask import request
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from . import CustomerFirm
from . import customer_firm_dto
from .service import CustomerFirmService
from .interface import CustomerFirmInterface

from ...utils.decorators import login_required, accepted_u_types, confirmation_required, employer_required


ns = Namespace("CustomerFirm", description="Customer Firm Related Operations")  # noqa
ns.add_model(customer_firm_dto.name, customer_firm_dto)


@ns.route('/')
class CustomerFirmResource(Resource):
    '''Get all CustomerFirm Firms'''
    # @login_required
    # @accepted_u_types('admin')
    @ns.marshal_list_with(customer_firm_dto, envelope='data')
    def get(self) -> List[CustomerFirm]:
        '''List Of Registered CustomerFirm Firms'''
        return CustomerFirmService.get_all()

    @ns.marshal_with(customer_firm_dto)
    @ns.expect(customer_firm_dto, validate=True)
    def post(self):
        """Create A Single Customer Firm"""
        customer_firm_data: CustomerFirmInterface = request.json
        return CustomerFirmService.create(customer_firm_data)


@ns.route('/<int:customer_firm_id>')
@ns.param('customer_firm_id', 'Customer firm ID')
class CustomerFirmIdResource(Resource):
    # @login_required
    # @accepted_u_types('admin')
    @ns.marshal_with(customer_firm_dto)
    def get(self, customer_firm_id: int) -> CustomerFirm:
        '''Get One CustomerFirm'''
        return CustomerFirmService.get_by_id(customer_firm_id)

    # @login_required
    # @accepted_u_types('admin')
    def delete(self, customer_firm_id: int) -> Response:
        '''Delete A Single CustomerFirm'''
        return CustomerFirmService.delete_by_id(customer_firm_id)
