from datetime import date, timedelta
import os
import datetime
import uuid
from typing import List

from werkzeug.exceptions import Conflict, NotFound, Unauthorized, UnsupportedMediaType
from flask import g, current_app
from app.extensions import db

from .model import SellerFirm
from .schema import seller_firm_dto

from ...utils.service import InputService

BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config['BASE_PATH_STATIC_DATA_SELLER_FIRM']

class SellerFirmService:
    @staticmethod
    def get_all() -> List[SellerFirm]:
        seller_firms = SellerFirm.query.all()
        return seller_firms

    @staticmethod
    def get_by_id(public_id: str) -> SellerFirm:
        seller_firm = SellerFirm.query.filter_by(public_id = public_id).first()
        if seller_firm:
            return seller_firm


    @staticmethod
    def update(public_id: str, data_changes: dict) -> SellerFirm:
        seller_firm = SellerFirmService.get_by_id(public_id)
        seller_firm.update(data_changes)
        db.session.commit()
        return seller_firm

    @staticmethod
    def delete_by_id(public_id: str):
        #check if accounting business exists in db
        seller_firm = SellerFirm.query.filter(SellerFirm.public_id == public_id).first()
        if seller_firm:
            db.session.delete(seller_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Seller firm (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This accounting firm does not exist.')

    @staticmethod
    def create_seller_firm(seller_firm_data: dict) -> SellerFirm:

        new_seller_firm = SellerFirm(
            claimed = seller_firm_data.get('claimed'),
            created_by = seller_firm_data.get('created_by'),
            name = seller_firm_data.get('name'),
            address = seller_firm_data.get('address'),
            establishment_country_code = seller_firm_data.get('establishment_country_code'),
            accounting_firm_id = seller_firm_data.get('accounting_firm_id'),
            accounting_firm_client_id = seller_firm_data.get('accounting_firm_client_id')
        )

        #add seller firm to db
        db.session.add(new_seller_firm)
        db.session.commit()

        return new_seller_firm



    @staticmethod
    #kwargs can contain: seller_firm_id
    def process_seller_firm_information_files_upload(seller_firm_information_files: list, **kwargs):
        file_type = 'seller_firm'
        df_encoding = None
        delimiter = None
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        claimed = False
        user_id = g.user.id
        accounting_firm_id = g.user.employer_id


        for file in seller_firm_information_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            SellerFirmService.process_seller_firm_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, claimed=claimed, user_id=user_id, accounting_firm_id=accounting_firm_id, **kwargs)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(seller_firm_information_files)))
        }

        return response_object


    # celery task !!!
    @staticmethod
    def process_seller_firm_information_file(file_path_in: str, file_type: str, df_encoding, delimiter, basepath: str, **kwargs) -> list:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = SellerFirmService.create_seller_firms(df, file_path_in, **kwargs)

        InputService.move_file_to_out(file_path_in, file_type)


        return response_objects




    @staticmethod
    def create_seller_firms(df, file_path_in: str, **kwargs): #upload only for tax auditors
        error_counter = 0
        total_number_items = len(df.index)
        input_type = 'seller firm'  # only used for response objects

        for i in range(total_number_items):

            seller_firm_data = {
                'claimed': kwargs['claimed'],
                'created_by': kwargs['user_id'],
                'name': InputService.get_str_or_None(df, i, column='seller_firm_name'),
                'address': InputService.get_str_or_None(df, i, column='address'),
                'establishment_country_code': InputService.get_str(df, i, column='establishment_country_code'),
                'accounting_firm_id': kwargs['accounting_firm_id'],
                'accounting_firm_client_id': InputService.get_str(df, i, column='accounting_firm_client_id'),
            }

            try:
                SellerFirmService.create_seller_firm(seller_firm_data)

            except:
                db.session.rollback()
                error_counter += 1

            db.session.commit()

        response_objects = InputService.create_input_response_objects(file_path_in, input_type, total_number_items, error_counter)

        return response_objects




    # @staticmethod
    # def handle_redundancy(seller_firm_id: int) -> int:
    #     seller_firm: SellerFirm = SellerFirm.query.filter_by(id=seller_firm_id).first()

    #     if seller_firm:
    #         redundancy_counter = 1
    #     else:
    #         redundancy_counter = 0

    #     return redundancy_counter























# # List all files in a directory using scandir(): Returns an iterator of all the objects in a directory including file attribute information


#  @staticmethod
#     def create_unclaimed_seller_firm(tax_auditor, seller_firm_data) -> SellerFirm:
#         amazon_seller_id = seller_firm_data.get('amazon_seller_id')
#         company_name = seller_firm_data.get('company_name')

#         if amazon_seller_id and company_name:
#             seller_firm_asi = SellerFirm.query.filter_by(amazon_seller_id=amazon_seller_id).first()
#             seller_firm_cn = SellerFirm.query.filter_by(company_name=company_name).first()

#             if seller_firm_asi and seller_firm_cn:
#                 if seller_firm_asi != seller_firm_cn:
#                     seller_firm = seller_firm_asi
#                     if seller_firm.accounting_firm_id != tax_auditor.employer_id:
#                         response_object = {
#                             'status': 'error',
#                             'message': 'The details provided point to two different companies that have already been registered. Please establish a client connection with the company instead.'
#                         }
#                         return response_object

#                     else:
#                         response_object = {
#                                 'status': 'error',
#                                 'message': 'The details provided point to a company that has already been registered. Please establish a client connection with the company instead.'
#                             }
#                         return response_object

#             elif seller_firm_asi and not seller_firm_cn:
#                 response_object = {
#                     'status': 'error',
#                     'message': 'The amazon unique identifier provided points to a company that has already been registered and the company name does not match. Please recheck the provided details.'
#                     }
#                 return response_object
#             elif seller_firm_cn and not seller_firm_asi:
#                 response_object = {
#                     'status': 'error',
#                     'message': 'The company name provided points to a company that has already been registered and the amazon unique identifier does not match. Please recheck the provided details.'
#                 }
#                 return response_object
#             elif not seller_firm_cn and not seller_firm_asi:
#                 accounting_firm_client_id = seller_firm_data.get('accounting_firm_client_id')
#                 # create new unclaimed seller firm
#                 new_unclaimed_seller_firm = SellerFirm(
#                     claimed=False,
#                     amazon_seller_id=amazon_seller_id,
#                     accounting_firm_id=tax_auditor.employer_id,
#                     accounting_firm_client_id=accounting_firm_client_id
#                 )
#                 #add seller to db
#                 db.session.add(new_unclaimed_seller_firm)
#                 db.session.commit()
#                 # this implementation implies that the seller with an unclaimed account is not in control if or if not the tax_auditor sets her as her client
#                 # the pattern for claimed accounts requires authorization by the seller.
#                 return seller_firm
#         else:
#             response_object = {
#                 'status': 'error',
#                 'message': 'Please provide a valid amazon unique identifier and a valid company name.'
#             }
#             return response_object
