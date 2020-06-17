from typing import List

from flask import request
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from . import Admin
from . import admin_dto
from .service import AdminService
from .interface import AdminInterface

from ...utils.decorators import login_required, accepted_u_types, confirmation_required


ns = Namespace("Admin", description="Accounting Firm Related Operations")  # noqa
ns.add_model(admin_dto.name, admin_dto)


@ns.route('/')
class AdminResource(Resource):
    '''Get all Admin'''
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_list_with(admin_dto, envelope='data')
    def get(self) -> List[Admin]:
        '''List Of Registered Admin Firms'''
        return AdminService.get_all()

    @accepted_u_types('admin')
    @ns.expect(admin_dto, validate=True)
    @ns.marshal_with(admin_dto)
    def post(self):
        """Create A Single Seller Firm"""
        admin_data: AdminInterface = request.json
        return AdminService.create(admin_data)


@ns.route('/<int:admin_id>')
@ns.param('admin_id', 'Seller firm ID')
class AdminIdResource(Resource):
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_with(admin_dto)
    def get(self, admin_id: int) -> Admin:
        '''Get One Admin'''
        return AdminService.get_by_id(admin_id)

    @login_required
    @accepted_u_types('admin')
    def delete(self, admin_id: int) -> Response:
        '''Delete A Single Admin'''
        return AdminService.delete_by_id(admin_id)
