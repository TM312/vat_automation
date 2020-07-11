from typing import List, Dict, BinaryIO
import os
import pandas as pd
from datetime import date, timedelta, datetime
from flask import g, current_app
from app.extensions import db

from . import DistanceSale
from .interface import DistanceSaleInterface
from ..utils.service import InputService




class DistanceSaleService:
    @staticmethod
    def get_all() -> List[DistanceSale]:
        return DistanceSale.query.all()

    @staticmethod
    def get_by_id(distance_sale_id: int) -> DistanceSale:
        return DistanceSale.query.get(distance_sale_id)

    @staticmethod
    def get_by_public_id(distance_sale_public_id: str) -> DistanceSale:
        return DistanceSale.query.filter_by(public_id = distance_sale_public_id).first()

    @staticmethod
    def update(distance_sale_public_id: DistanceSale, data_changes: DistanceSaleInterface) -> DistanceSale:
        distance_sale.update(data_changes)
        db.session.commit()
        return distance_sale

    @staticmethod
    def update_by_public_id(distance_sale_public_id: str, data_changes: DistanceSaleInterface) -> DistanceSale:
        distance_sale = DistanceSaleService.get_by_public_id(distance_sale_public_id)
        if distance_sale:
            distance_sale.update(data_changes)
            db.session.commit()
            return distance_sale

    @staticmethod
    def create_by_seller_firm_public_id(seller_firm_public_id: str, distance_sale_data: DistanceSaleInterface) -> DistanceSale:
        from ..business.seller_firm.service import SellerFirmService

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            DistanceSaleService.handle_redundancy(seller_firm.id, distance_sale_data['arrival_country_code'], distance_sale_data['valid_from'])

            distance_sale_data['seller_firm_id'] = seller_firm.id
            distance_sale = DistanceSaleService.create(distance_sale_data)

        return distance_sale




    @staticmethod
    def delete_by_id(distance_sale_id: int) -> List[int]:
        distance_sale = DistanceSaleService.get_by_id(distance_sale_id)
        if not distance_sale:
            return []
        db.session.delete(distance_sale)
        db.session.commit()
        return [distance_sale_id]

    @staticmethod
    def delete_by_public_id(distance_sale_public_id: str) -> List[int]:
        distance_sale = DistanceSaleService.get_by_public_id(distance_sale_public_id)
        if not distance_sale:
            return []
        db.session.delete(distance_sale)
        db.session.commit()
        return [distance_sale_public_id]

    @staticmethod
    def process_single_submit(seller_firm_public_id: str, distance_sale_data: DistanceSaleInterface):

        distance_sale_data['created_by'] = g.user.id
        distance_sale_data['valid_from'] = datetime.strptime(distance_sale_data['valid_from'], "%Y-%m-%d").date()

        if not 'valid_to' in distance_sale_data:
            TAX_DEFAULT_VALIDITY = current_app.config['TAX_DEFAULT_VALIDITY']
            distance_sale_data['valid_to'] = TAX_DEFAULT_VALIDITY

        else:
            distance_sale_data['valid_to'] = datetime.strptime(distance_sale_data['valid_to'], "%Y-%m-%d").date()

        distance_sale = DistanceSaleService.create_by_seller_firm_public_id(seller_firm_public_id, distance_sale_data)

        return distance_sale



    @staticmethod
    #kwargs can contain: seller_firm_public_id
    def process_distance_sale_files_upload(distance_sale_information_files: List[BinaryIO], **kwargs) -> Dict:

        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config['BASE_PATH_STATIC_DATA_SELLER_FIRM']

        file_type = 'distance_sale_list'
        df_encoding = 'utf-8'
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        user_id = g.user.id
        delimiter = ';'

        for file in distance_sale_information_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            DistanceSaleService.process_distance_sale_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, **kwargs)

        response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(distance_sale_information_files)))
        }

        return response_object



    # celery task !!
    @staticmethod
    def process_distance_sale_information_file(file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, **kwargs) -> List[Dict]:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)
        response_objects = DistanceSaleService.create_distance_sales(df, file_path_in, user_id, **kwargs)

        InputService.move_file_to_out(file_path_in, basepath, file_type)


        return response_objects




    @staticmethod
    def create_distance_sales(df: pd.DataFrame, file_path_in: str, user_id: int, **kwargs) -> List[Dict]:
        from ..business.seller_firm.service import SellerFirmService

        redundancy_counter = 0
        error_counter = 0
        total_number_distance_sales = len(df.index)
        input_type = 'distance_sale' # only used for response objects

        for i in range(total_number_distance_sales):

            seller_firm_id = SellerFirmService.get_seller_firm_id(df=df, i=i, **kwargs)
            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            valid_to = InputService.get_date_or_None(df, i, column='valid_to')
            arrival_country_code = InputService.get_str(df, i, column='arrival_country_code')
            active = InputService.get_bool(df, i, column='active', value_true=True)

            if not valid_from:
                valid_from = date.today()
            if not valid_to:
                TAX_DEFAULT_VALIDITY = current_app.config['TAX_DEFAULT_VALIDITY']
                valid_to = TAX_DEFAULT_VALIDITY

            if seller_firm_id:
                redundancy_counter += DistanceSaleService.handle_redundancy(seller_firm_id, arrival_country_code, valid_from)
                distance_sale_data = {
                    'created_by': user_id,
                    'original_filename' : os.path.basename(file_path_in),
                    'seller_firm_id': seller_firm_id,
                    'valid_from': valid_from,
                    'valid_to': valid_to,
                    'platform_code': 'AMZ',
                    'arrival_country_code': arrival_country_code,
                    'active': active
                }



                try:
                    new_distance_sale = DistanceSaleService.create(distance_sale_data)

                except:
                    db.session.rollback()

                    error_counter += 1

            else:
                error_counter += 1

        response_objects = InputService.create_input_response_objects(file_path_in, input_type, total_number_distance_sales, error_counter, redundancy_counter=redundancy_counter)

        return response_objects


    @staticmethod
    def create(distance_sale_data: DistanceSaleInterface) -> DistanceSale:

        new_distance_sale = DistanceSale(
            created_by = distance_sale_data.get('created_by'),
            original_filename = distance_sale_data.get('original_filename'),
            valid_from = distance_sale_data.get('valid_from'),
            valid_to = distance_sale_data.get('valid_to'),
            platform_code = distance_sale_data.get('platform_code'),
            seller_firm_id=distance_sale_data.get('seller_firm_id'),
            arrival_country_code = distance_sale_data.get('arrival_country_code'),
            active = distance_sale_data.get('active')
        )

        #add seller firm to db
        db.session.add(new_distance_sale)

        db.session.commit()

        return new_distance_sale



    @staticmethod
    def handle_redundancy(seller_firm_id: int, arrival_country_code: str, valid_from: date) -> int:
        redundancy_counter = 0
        distance_sale = DistanceSale.query.filter(DistanceSale.arrival_country_code == arrival_country_code, DistanceSale.seller_firm_id == seller_firm_id, DistanceSale.valid_to >= valid_from).first()
        # if an distance_sale with the same sku for the specified validity period already exists, it is being updated or deleted.
        if distance_sale:
            if distance_sale.valid_from >= valid_from:
                db.session.delete(distance_sale)

            else:
                data_changes = {
                    'valid_to': valid_from - timedelta(days=1)
                }
                distance_sale.update(data_changes)
                redundancy_counter += 1

        return redundancy_counter


    @staticmethod
    def get_status(platform_code: str, seller_firm_id: int, arrival_country_code: str, tax_date: date) -> bool:
        distance_sale=DistanceSale.query.filter_by(DistanceSale.platform_code==platform_code, DistanceSale.seller_firm_id==seller_firm_id, DistanceSale.arrival_country_code==arrival_country_code, DistanceSale.valid_from<=tax_date, DistanceSale.valid_to>=tax_date).first()
        if distance_sale:
            return distance_sale.active
