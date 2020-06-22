from typing import List, BinaryIO

from flask import request, g
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from . import TaxAuditor
from . import tax_auditor_dto, tax_auditor_dto_admin
from .service import TaxAuditorService
from .interface import TaxAuditorInterface

from ...utils.decorators import login_required, accepted_u_types, confirmation_required
from ...utils.service import TemplateService



ns = Namespace("TaxAuditor", description="TaxAuditor Related Operations")  # noqa
ns.add_model(tax_auditor_dto.name, tax_auditor_dto)
ns.add_model(tax_auditor_dto_admin.name, tax_auditor_dto_admin)
# https://flask-restx.readthedocs.io/en/latest/api.html#flask_restx.Model
# https://github.com/python-restx/flask-restx/blob/014eb9591e61cd3adbbd29a38b76df6a688f067b/flask_restx/namespace.py


@ns.route('/')
class TaxAuditorResource(Resource):
    '''Get all TaxAuditor'''
    #@login_required
    #@accepted_u_types('admin')
    @ns.marshal_list_with(tax_auditor_dto, envelope='data')
    def get(self) -> List[TaxAuditor]:
        '''List Of Registered TaxAuditor Firms'''
        return TaxAuditorService.get_all()

    #@accepted_u_types('admin')
    @ns.expect(tax_auditor_dto, validate=True)
    @ns.marshal_with(tax_auditor_dto)
    def post(self):
        """Create A Single Seller Firm"""
        admin_data: TaxAuditorInterface = request.json
        return TaxAuditorService.create(admin_data)


@ns.route('/self')
class TaxAuditorSelfResource(Resource):
    '''Get all TaxAuditor'''
    @login_required
    #@accepted_u_types('admin')
    @ns.marshal_list_with(tax_auditor_dto, envelope='data')
    def get(self) -> List[TaxAuditor]:
        '''List Of Registered TaxAuditor Firms'''
        return TaxAuditorService.get_by_id(g.user.id)



@ns.route('/<int:tax_auditor_id>')
@ns.param('tax_auditor_id', 'Seller firm ID')
class TaxAuditorIdResource(Resource):
    #@login_required
    #@accepted_u_types('admin')
    @ns.marshal_with(tax_auditor_dto, envelope='data')
    def get(self, tax_auditor_id: int) -> TaxAuditor:
        '''Get One TaxAuditor'''
        return TaxAuditorService.get_by_id(tax_auditor_id)

    #@login_required
    @accepted_u_types('admin')
    def delete(self, tax_auditor_id: int) -> Response:
        '''Delete A Single TaxAuditor'''
        return TaxAuditorService.delete_by_id(tax_auditor_id)

    #@ns.expect(tax_auditor_dto, validate=True)
    @ns.marshal_with(tax_auditor_dto)
    def put(self, tax_auditor_id: int) -> TaxAuditor:
        """Update Single TaxAuditor"""

        changes: TaxAuditorInterface = request.parsed_obj
        return TaxAuditorService.update(tax_auditor_id, changes)
