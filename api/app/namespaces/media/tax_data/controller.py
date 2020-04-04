from typing import List

from flask import request
from flask import g, current_app

from flask.wrappers import Response
from werkzeug.utils import secure_filename
from flask_restx import Namespace, Resource
from ...utils.decorators.auth import login_required, accepted_roles, confirmation_required


#from .schema import tax_data_dto
from .service import TaxDataService


ns = Namespace("tax_data", description="Tax Data Related Operations")  # noqa
#ns.add_model(tax_data_dto.name, tax_data_dto)


@ns.route("/")
class AdminTaxDataListResource(Resource):
    def get(self):
        """List Of Registered TaxDatas"""
        return {'response': 'Hello, world'}

# @ns.route("/")
# class AdminTaxDataListResource(Resource):
#     """Get all Tax Datas"""
#     @login_required
#     @accepted_roles('admin')
#     @ns.marshal_list_with(tax_data_dto, envelope='data')
#     def get(self) -> List[TaxData]:
#         """List Of Registered TaxDatas"""
#         return TaxDataService.get_all()


# @ns.route("/<string:file_name>")
# @ns.param("file_name", "File name")
# class AdminTaxDataIdResource(Resource):
#     @login_required
#     @accepted_roles('admin')
#     @ns.marshal_with(tax_data_dto)
#     def get(self, public_id: str) -> TaxData:
#         """Get One TaxData"""
#         return TaxDataService.get_by_id(public_id)

#     @login_required
#     @accepted_roles('admin')
#     def delete(self, public_id: str) -> Response:
#         """Delete A Single TaxData"""
#         return TaxDataService.delete_by_id(public_id)


@ns.route("/upload")
class TaxDataResource(Resource):
    # @login_required
    # @confirmation_required
    # @ns.expect(tax_data_dto, validate=True)
    def post(self):
        """Create A Tax Data Entry And Store The Corresponding File"""
        print("POST request received")
        user = "f997f796-a605-4175-8fae-3de2d0c773a6"  # g.user
        uploaded_files = request.files.getlist("files")
        print("POST file received")
        print('uploaded_files')
        print(uploaded_files)
        return TaxDataService.upload_input(user, uploaded_files)


@ns.route("/download/<string:filename>")
class TaxDataResource(Resource):
    # @login_required
    # @confirmation_required
    # @ns.expect(tax_data_dto, validate=True)
    def get(self, filename):
        """Download A Tax Data File"""
        user = "f997f796-a605-4175-8fae-3de2d0c773a6"  # g.user
        return TaxDataService.download_file(user, filename)
