from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource

from .service import DistanceSaleService

from ...utils.decorators import login_required, employer_required

ns = Namespace("Amazon", description="Amazon Related Operations")  # noqa
#ns.add_model(tax_record_dto.name, tax_record_dto)




@ns.route("/csv")
class DistanceSalesResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    #@ns.expect(tax_record_dto, validate=True)
    def post(self):
        distance_sale_information_files: List[BinaryIO] = request.files.getlist("files")
        return DistanceSaleService.process_distance_sale_files_upload(distance_sale_information_files)
