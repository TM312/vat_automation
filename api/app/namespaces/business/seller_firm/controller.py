from typing import List

from flask import request, g
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from . import SellerFirm
from . import seller_firm_dto, seller_firm_sub_dto
from .service import SellerFirmService
from .interface import SellerFirmInterface

from ...utils.decorators import login_required, accepted_u_types, confirmation_required, employer_required


ns = Namespace("SellerFirm", description="Seller Firm Related Operations")  # noqa
ns.add_model(seller_firm_dto.name, seller_firm_dto)
ns.add_model(seller_firm_sub_dto.name, seller_firm_sub_dto)



@ns.route('/')
class SellerFirmResource(Resource):
    '''Get all SellerFirm Firms'''
    #@login_required
    #@accepted_u_types('admin')
    @ns.marshal_list_with(seller_firm_dto, envelope='data')
    def get(self) -> List[SellerFirm]:
        '''List Of Registered SellerFirm Firms'''
        return SellerFirmService.get_all()

    @ns.expect(seller_firm_dto, validate=True)
    @ns.marshal_with(seller_firm_dto)
    def post(self):
        """Create A Single Seller Firm"""
        seller_firm_data: SellerFirmInterface = request.json
        return SellerFirmService.create(seller_firm_data)


@ns.route('/<string:seller_firm_public_id>')
@ns.param('seller_firm_public_id', 'Seller firm ID')
class SellerFirmIdResource(Resource):
    @login_required
    #@accepted_u_types('admin')
    @ns.marshal_with(seller_firm_dto, envelope='data')
    def get(self, seller_firm_public_id: str) -> SellerFirm:
        '''Get One SellerFirm'''
        return SellerFirmService.get_by_public_id(seller_firm_public_id)

    @login_required
    # @accepted_u_types('admin')
    def delete(self, seller_firm_public_id: str) -> Response:
        '''Delete A Single SellerFirm'''
        return SellerFirmService.delete_by_public_id(seller_firm_public_id)


@ns.route("/<string:seller_firm_public_id>/upload")
class SellerFirmInformationResource(Resource):
    @login_required
    def post(self, seller_firm_public_id):
        """Upload data for the indicated seller firm"""
        seller_firm_files: List[BinaryIO] = request.files.getlist("files")
        return SellerFirmService.process_static_data_upload(seller_firm_public_id, seller_firm_files)


@ns.route('/as_client')
class SellerFirmAsClientResource(Resource):
    @login_required
    #@accepted_u_types('admin')
    @ns.expect(SellerFirmInterface, validate=True)
    @ns.marshal_with(seller_firm_sub_dto, envelope='data')
    def post(self) -> SellerFirm:
        """Create A Single Seller Firm"""
        seller_firm_data: SellerFirmInterface = request.json
        return SellerFirmService.create_as_client(seller_firm_data)




@ns.route("/csv")
class SellerFirmInformationResource(Resource):
    @login_required
    def post(self):
        """Create an unclaimed seller firm as a client"""
        seller_firm_information_files: List[BinaryIO] = request.files.getlist("files")
        return SellerFirmService.process_seller_firm_information_files_upload(seller_firm_information_files, claimed=False)
