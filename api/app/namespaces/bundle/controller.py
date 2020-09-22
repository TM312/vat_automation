from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Bundle
from . import bundle_dto, bundle_admin_dto, bundle_sub_dto
from .service import BundleService
from .interface import BundleInterface
from app.namespaces.utils.decorators import login_required


ns = Namespace("Bundle", description="Bundle Related Operations")  # noqa
ns.add_model(bundle_dto.name, bundle_dto)
ns.add_model(bundle_admin_dto.name, bundle_admin_dto)
ns.add_model(bundle_sub_dto.name, bundle_sub_dto)



@ns.route("/")
class BundleResource(Resource):
    """Bundles"""
    @login_required
    @ns.marshal_list_with(bundle_dto, envelope='data')
    def get(self) -> List[Bundle]:
        """Get all Bundles"""
        return BundleService.get_all()

    @login_required
    @ns.expect(bundle_dto, validate=True)
    @ns.marshal_with(bundle_dto)
    def post(self) -> Bundle:
        """Create a Single Bundle"""
        return BundleService.create()


@ns.route("/<string:bundle_public_id>")
@ns.param("bundle_public_id", "Bundle database ID")
class BundleIdResource(Resource):

    @login_required
    @ns.marshal_with(bundle_dto, envelope='data')
    def get(self, bundle_public_id: str) -> Bundle:
        """Get Single Bundle"""
        return BundleService.get_by_public_id(bundle_public_id)

    @login_required
    def delete(self, bundle_public_id: str) -> Response:
        """Delete Single Bundle"""
        from flask import jsonify

        id = BundleService.delete_by_public_id(bundle_public_id)
        return jsonify(dict(status="Success", id=id))

    @login_required
    @ns.expect(bundle_dto, validate=True)
    @ns.marshal_with(bundle_dto)
    def put(self, bundle_public_id: str) -> Bundle:
        """Update Single Bundle"""

        data_changes: BundleInterface = request.parsed_obj
        return BundleService.update_by_public_id(Bundle, data_changes)
