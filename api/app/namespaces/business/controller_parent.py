from typing import List
from uuid import UUID

from flask import request
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from . import Business
from . import business_dto, business_sub_dto, business_admin_dto
from .service_parent import BusinessService

from ..utils.decorators import login_required, accepted_u_types


ns = Namespace('Business', description='Business Related Operations')  # noqa
ns.add_model(business_dto.name, business_dto)
ns.add_model(business_sub_dto.name, business_sub_dto)
ns.add_model(business_admin_dto.name, business_admin_dto)


@ns.route('/')
class AdminBusinessListResource(Resource):
    '''Get all Business Firms'''
    #@login_required
    #@accepted_u_types('admin')
    @ns.marshal_list_with(business_dto, envelope='data')
    def get(self) -> List[Business]:
        '''List Of Registered Business Firms'''
        return BusinessService.get_all()


@ns.route('/<string:public_id>')
@ns.param('public_id', 'Public accounting business ID')
class AdminBusinessIdResource(Resource):
    #@login_required
    #@accepted_u_types('admin')
    @ns.marshal_with(business_dto)
    def get(self, public_id: str) -> Business:
        '''Get One Business'''
        return BusinessService.get_by_id(UUID(public_id))

    #@login_required
    #@accepted_u_types('admin')
    def delete(self, public_id: str) -> Response:
        '''Delete A Single Business'''
        return BusinessService.delete_by_id(UUID(public_id))
