from typing import List

from flask import request, g
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from .schema import seller_dto, seller_dto_admin
from .service import SellerService
from .model import Seller
from .interface import SellerInterface

from ...auth.interface import TokenInterface
from ...utils.decorators.auth import login_required, accepted_u_types, confirmation_required



ns = Namespace("Seller", description="Seller Related Operations")  # noqa
ns.add_model(seller_dto.name, seller_dto)
#ns.add_model(seller_dto_admin.name, seller_dto_admin)

# https://flask-restx.readthedocs.io/en/latest/api.html#flask_restx.Model
# https://github.com/python-restx/flask-restx/blob/014eb9591e61cd3adbbd29a38b76df6a688f067b/flask_restx/namespace.py


@ns.route("/")
class SellerResource(Resource):
    # @ns.param("public_id", "Public seller ID")
    @login_required
    @ns.marshal_with(seller_dto, envelope='data')
    def get(self) -> Seller:
        """ Current Seller Seller """
        return g.user

    @ns.expect(seller_dto, validate=True)
    def post(self):
        """Create A Single Seller"""
        seller_data: SellerInterface = request.json
        return SellerService.create_self(seller_data)

    @login_required
    def delete(self) -> Response:
        """Delete self"""
        return SellerService.delete_by_id(g.user.public_id)

    @login_required
    @ns.expect(seller_dto, validate=True)
    @ns.marshal_with(seller_dto)
    def put(self) -> Seller:
        """Update self"""
        data_changes: SellerInterface = request.json  # JSON body of a request
        seller = g.user
        return SellerService.update(seller, data_changes)
