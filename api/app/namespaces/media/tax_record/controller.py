from typing import List

from flask import request
from flask import g, current_app

from flask.wrappers import Response
from werkzeug.utils import secure_filename
from flask_restx import Namespace, Resource
from ...utils.decorators.auth import login_required, accepted_roles, confirmation_required


from .schema import tax_record_dto
from .service import TaxRecordService
from .model import TaxRecord


ns = Namespace("tax_record", description="Tax Data Related Operations")  # noqa
ns.add_model(tax_record_dto.name, tax_record_dto)


@ns.route("/")
class AdminTaxRecordListResource(Resource):

# @ns.route("/")
# class AdminTaxRecordListResource(Resource):
#     """Get all Tax Datas"""
#     @login_required
#     @accepted_roles('admin')
#     @ns.marshal_list_with(tax_record_dto, envelope='data')
#     def get(self) -> List[TaxRecord]:
#         """List Of Registered TaxRecords"""
#         return TaxRecordService.get_all()


# @ns.route("/<string:file_name>")
# @ns.param("file_name", "File name")
# class AdminTaxRecordIdResource(Resource):
#     @login_required
#     @accepted_roles('admin')
#     @ns.marshal_with(tax_record_dto)
#     def get(self, public_id: str) -> TaxRecord:
#         """Get One TaxRecord"""
#         return TaxRecordService.get_by_id(public_id)

#     @login_required
#     @accepted_roles('admin')
#     def delete(self, public_id: str) -> Response:
#         """Delete A Single TaxRecord"""
#         return TaxRecordService.delete_by_id(public_id)

@ns.route("/own")
class UserResource(Resource):
    """Get owned available Tax Records"""
    @login_required
    @ns.marshal_with(tax_record_dto, envelope='data')
    def get(self) -> List[TaxRecord]:
        """ List of owned Tax Records """
        user = g.user
        return TaxRecordService.get_own(user)
#     @login_required
#     @accepted_roles('admin')
#     @ns.marshal_list_with(tax_record_dto, envelope='data')
#     def get(self) -> List[TaxRecord]:
#         """List Of Registered TaxRecords"""
#         return TaxRecordService.get_all()


@ns.route("/upload")
class TaxRecordResource(Resource):
    @login_required
    # @confirmation_required
    # @ns.expect(tax_record_dto, validate=True)
    def post(self):
        """Create A Tax Data Entry And Store The Corresponding File"""
        print("POST request received")
        user = g.user  # "f997f796-a605-4175-8fae-3de2d0c773a6"
        uploaded_files = request.files.getlist("files")
        print("POST file received")
        print('uploaded_files')
        print(uploaded_files)
        return TaxRecordService.upload_input(user, uploaded_files)


@ns.route("/download/<string:activity_period>/<string:filename>")
class TaxRecordResource(Resource):
    @login_required
    # @confirmation_required
    # @ns.expect(tax_record_dto, validate=True)
    def get(self, activity_period, filename):
        """Download A Tax Data File"""
        #user = "f997f796-a605-4175-8fae-3de2d0c773a6"
        user = g.user
        return TaxRecordService.download_file(user, activity_period, filename)
