import os
from datetime import date, timedelta
from flask import g, current_app
from app.extensions import db

from .model import DistanceSale
from ...utils.service import InputService
from ...business.seller_firm.service import SellerFirmService





class DistanceSaleService:


    @staticmethod
    #kwargs can contain: seller_firm_id
    def process_distance_sale_files_upload(distance_sale_information_files: list, **kwargs) -> dict:
        BASE_PATH_STATIC_DATA_SELLER_FIRM = current_app.config['BASE_PATH_STATIC_DATA_SELLER_FIRM']

        file_type = 'distance_sale_list'
        df_encoding = None
        basepath = BASE_PATH_STATIC_DATA_SELLER_FIRM
        user_id = g.user.id
        delimiter = None

        for file in distance_sale_information_files:
            file_path_in = InputService.store_static_data_upload(file=file, file_type=file_type)
            DistanceSaleService.process_distance_sale_information_file(file_path_in, file_type, df_encoding, delimiter, basepath, user_id=user_id, **kwargs)

         response_object = {
            'status': 'success',
            'message': 'The files ({} in total) have been successfully uploaded and we have initialized their processing.'.format(str(len(distance_sale_information_files)))
        }

        return response_object



    # celery task !!
    @staticmethod
    def process_distance_sale_information_file(file_path_in: str, file_type: str, df_encoding, delimiter, basepath: str, **kwargs) -> list:

        df = InputService.read_file_path_into_df(file_path_in, df_encoding, delimiter)

        response_objects = DistanceSaleService.create_distance_sales(df, file_path_in, **kwargs)

        InputService.move_file_to_out(file_path_in, file_type)


        return response_objects




    @staticmethod
    def create_distance_sales(df, file_path_in: int, **kwargs) -> list:
        TAX_DEFAULT_VALIDITY = current_app.config['TAX_DEFAULT_VALIDITY']

        redundancy_counter = 0
        error_counter = 0
        total_number_distance_sales = len(df.index)
        input_type = 'distance_sale' # only used for response objects

        for i in range(total_number_distance_sales):

            seller_firm_id = SellerFirmService.get_seller_firm_id(df, i, **kwargs)
            valid_from = InputService.get_date_or_None(df, i, column='valid_from')
            valid_to = InputService.get_date_or_None(df, i, column='valid_to')
            arrival_country_code = InputService.get_str(df, i, column='arrival_country_code')
            distance_sale = InputService.get_str(df, i, column='distance_sale')

            if not valid_from:
                valid_from = date.today()
            if not valid_to:
                valid_to = valid_from + timedelta(days=TAX_DEFAULT_VALIDITY)

            if seller_firm_id:
                redundancy_counter += DistanceSaleService.handle_redundancy(public_id, channel_code)

                distance_sale_data = {
                    'created_by': kwargs['user_id'],
                    'original_filename' : os.path.basename(file_path_in),
                    'seller_firm_id': seller_firm_id,
                    'valid_from': valid_from,
                    'valid_to': valid_to,
                    'arrival_country_code': arrival_country_code,
                    'distance_sale': distance_sales
                }

                try:
                    new_distance_sale = DistanceSaleService.create_distance_sale(distance_sale_data)

                except:
                    db.session.rollback()

                    error_counter += 1

            else:
                error_counter += 1


        response_objects = InputService.create_input_response_objects(file_path, input_type, total_number_distance_sales, error_counter, redundancy_counter=redundancy_counter)

        return response_objects


    @staticmethod
    def create_distance_sale(distance_sale_data: dict) -> DistanceSale:

        new_distance_sale = DistanceSale(
            created_by = distance_sale_data.get('created_by'),
            original_filename = distance_sale_data.get('original_filename'),
            seller_firm_id = distance_sale_data.get('seller_firm_id'),
            valid_from = distance_sale_data.get('valid_from'),
            valid_to = distance_sale_data.get('valid_to'),
            arrival_country_code = distance_sale_data.get('arrival_country_code'),
            distance_sale = distance_sale_data.get('distance_sale')
        )

        #add seller firm to db
        db.session.add(new_distance_sale)
        db.session.commit()

        return new_distance_sale



    @staticmethod
    def handle_redundancy(seller_firm_id: int, arrival_country_code: str, valid_from: date) -> int:
        distance_sale: DistanceSale = DistanceSale.query.filter(DistanceSale.arrival_country_code == arrival_country_code, DistanceSale.seller_firm_id == seller_firm_id, DistanceSale.valid_to >= valid_from).first()

        # if an distance_sale with the same sku for the specified validity period already exists, it is being updated or deleted.
        if distance_sale:
           if distance_sale.valid_from >= valid_from:
                db.session.delete(distance_sale)

            else:
                data_changes = {
                    'valid_to': valid_from - timedelta(days=1)
                }
                distance_sale.update(data_changes)
                redundancy_counter = 1
        else:
            redundancy_counter = 0

        return redundancy_counter
