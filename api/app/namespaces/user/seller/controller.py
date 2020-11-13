from typing import List

from flask import request, g
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from . import Seller
from . import seller_dto, seller_dto_admin
from .service import SellerService
from .interface import SellerInterface

from app.namespaces.utils.decorators.auth import login_required, accepted_u_types, confirmation_required
from app.extensions import cache



ns = Namespace("Seller", description="Seller Related Operations")  # noqa
ns.add_model(seller_dto.name, seller_dto)
ns.add_model(seller_dto_admin.name, seller_dto_admin)

# https://flask-restx.readthedocs.io/en/latest/api.html#flask_restx.Model
# https://github.com/python-restx/flask-restx/blob/014eb9591e61cd3adbbd29a38b76df6a688f067b/flask_restx/namespace.py


@ns.route('/')
class SellerResource(Resource):
    '''Get all Seller'''
    @login_required
    @accepted_u_types('admin')
    @cache.cached(timeout=60)
    @ns.marshal_list_with(seller_dto, envelope='data')
    def get(self) -> List[Seller]:
        '''List Of Registered Seller Firms'''
        return SellerService.get_all()

    @login_required
    @accepted_u_types('admin', 'seller')
    @ns.expect(seller_dto, validate=True)
    @ns.marshal_with(seller_dto)
    def post(self):
        """Create A Single Seller Firm"""
        seller_data: SellerInterface = request.json
        return SellerService.create(seller_data)


@ns.route('/self')
class SellerSelfResource(Resource):
    '''Get Seller Self'''
    @login_required
    @accepted_u_types('admin', 'seller')
    @ns.marshal_with(seller_dto, envelope='data')
    def get(self) -> List[Seller]:
        return SellerService.get_by_id(g.user.id)



@ns.route('/<int:seller_id>')
@ns.param('seller_id', 'Seller firm ID')
class SellerIdResource(Resource):
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_with(seller_dto)
    def get(self, seller_id: int) -> Seller:
        '''Get One Seller'''
        return SellerService.get_by_id(seller_id)

    @login_required
    @accepted_u_types('admin')
    def delete(self, seller_id: int) -> Response:
        '''Delete A Single Seller'''
        return SellerService.delete_by_id(seller_id)
