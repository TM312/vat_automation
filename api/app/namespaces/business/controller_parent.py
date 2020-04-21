from typing import List

from flask import request
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from .schema import business_dto
from .service import BusinessService
from .model import Business

from ...auth.interface import TokenInterface
from ...utils.decorators.auth import login_required, accepted_u_types


ns = Namespace("Business", description="Business Related Operations")  # noqa
ns.add_model(business_dto.name, business_dto)


@ns.route("/")
class AdminAccountingListResource(Resource):
    """Get all Accounting Firms"""
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_list_with(business_dto, envelope='data')
    def get(self) -> List[Accounting]:
        """List Of Registered Accounting Firms"""
        return BusinessService.get_all()


@ns.route("/<string:public_id>")
@ns.param("public_id", "Public accounting business ID")
class AdminAccountingIdResource(Resource):
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_with(business_dto)
    def get(self, public_id: str) -> Business:
        """Get One Accounting"""
        return BusinessService.get_by_id(public_id)

    @login_required
    @accepted_u_types('admin')
    def delete(self, public_id: str) -> Response:
        """Delete A Single Accounting Business"""
        return BusinessService.delete_by_id(public_id)
