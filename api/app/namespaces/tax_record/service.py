import pandas as pd
from datetime import date
from flask import g, current_app, send_from_directory
from typing import List, BinaryIO, Dict, Union
from uuid import UUID

from app.extensions import db

from werkzeug.exceptions import UnprocessableEntity, InternalServerError, Unauthorized, NotFound

from .interface import TaxRecordDictInterface, TaxRecordInterface
from . import TaxRecord

from ..utils.service import HelperService, NotificationService, InputService, CalcService
from ..utils import TransactionNotification
from ..transaction import Transaction
from ..transaction_input import TransactionInput
#from ..transaction_input.service import TransactionInputService


class TaxRecordService:
    @staticmethod
    def get_all() -> List[TaxRecord]:
        tax_records = TaxRecord.query.all()
        return tax_records

    @staticmethod
    def get_by_public_id(tax_record_public_id: str) -> TaxRecord:
        return TaxRecord.query.filter_by(public_id=tax_record_public_id).first()

    @staticmethod
    def get_all_by_seller_firm_public_id(seller_firm_public_id: str) -> List[TaxRecord]:
        tax_records = TaxRecord.query.filter_by(public_id=seller_firm_public_id).all()
        return tax_records

    @staticmethod
    def delete_by_public_id(seller_firm_public_id: str):
        tax_record = TaxRecord.query.filter(TaxRecord.public_id == seller_firm_public_id).first()
        if tax_record:
            db.session.delete(tax_record)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Transaction input (public_id: {}) has been successfully deleted.'.format(seller_firm_public_id)
            }
            return response_object
        else:
            raise NotFound('This transaction input does not exist.')


    def download_tax_record(public_id: str):
        from ..business.seller_firm import SellerFirm
        BASE_PATH_TAX_RECORD_DATA_SELLER_FIRM = current_app.config['BASE_PATH_TAX_RECORD_DATA_SELLER_FIRM']

        tax_record = TaxRecord.query.filter_by(public_id = public_id).first()
        if tax_record:
            seller_firm = SellerFirm.query.filter_by(id = seller_firm_id).first()
            if g.user.employer_id == tax_record.seller_firm_id or seller_firm in g.user.employer.clients:
                send_from_directory(directory=BASE_PATH_TAX_RECORD_DATA_SELLER_FIRM, filename=tax_record.filename, as_attachment=True)
            else:
                raise Unauthorized('You are not authorized to retrieve a tax record from the seller firm associated with the id {}'.format(public_id))

        else:
            raise NotFound('A Tax Record with the given ID does not exist.')



    @staticmethod
    def generate_tax_record(start_date_str: str, end_date_str: str, seller_firm_public_id: UUID, tax_jurisdiction_code: str) -> Dict:
        from ..business.seller_firm import SellerFirm
        BASE_PATH_TAX_RECORD_DATA_SELLER_FIRM = current_app.config['BASE_PATH_TAX_RECORD_DATA_SELLER_FIRM']

        seller_firm = SellerFirm.query.filter_by(public_id = seller_firm_public_id)
        if g.user.employer_id == seller_firm.accounting_firm_id:
            user_id = g.user.id

            #!!! call as async celery task
            TaxRecordService.save_as_file(start_date_str, end_date_str, seller_firm_public_id, BASE_PATH_TAX_RECORD_DATA_SELLER_FIRM, user_id, tax_jurisdiction_code)


            response_object = {
                'status': 'success',
                'message': 'A tax record for the period {}-{} is being generated.'.format(start_date_str, end_date_str)
            }
            return response_object

        else:
            raise Unauthorized('You are not authorized to retrieve tax records for this seller firm. Please make sure to establish a client relationship between your employer and the seller firm first.')



    @staticmethod
    def create_by_seller_firm_public_id(seller_firm_public_id: str, tax_record_data_raw: TaxRecordInterface):
        from ..business.seller_firm.service import SellerFirmService
        from ..transaction.service import TransactionService
        from ..tax.vatin.service import VATINService
        from ..tax.vatin import VATIN
        from ..country.service import CountryService

        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:

            start_date = HelperService.get_date_from_str(tax_record_data_raw.get('start_date'), '%Y-%m-%d')
            end_date = HelperService.get_date_from_str(tax_record_data_raw.get('end_date'), '%Y-%m-%d')
            tax_jurisdiction_code = tax_record_data_raw.get('tax_jurisdiction_code')

            tax_jurisdiction = CountryService.get_by_code(tax_jurisdiction_code)
            if not tax_jurisdiction:
                raise NotFound('Country not recognized.')

            vatin = VATINService.get_by_country_code_seller_firm_id(tax_jurisdiction_code, seller_firm.id)

            if not isinstance(vatin, VATIN):
                raise NotFound('A VATIN for the indicated tax jurisdiction does not exist for this seller firm.')


            transactions = TransactionService.get_by_validity_tax_jurisdiction_seller_firm(start_date, end_date, seller_firm.id, tax_jurisdiction_code)

            if not isinstance(transactions, list) or len(transactions) == 0:
                raise UnprocessableEntity('There are no transactions by this seller for this period and tax jurisdiction.')

            else:


                sales = [transaction for transaction in transactions if transaction.type_code == 'SALE']
                refunds = [transaction for transaction in transactions if transaction.type_code == 'REFUND']
                acquisitions = [transaction for transaction in transactions if transaction.type_code == 'ACQUISITION']


                # LOCAL SALES
                local_sales_sales_invoice_amount_net = TaxRecordService.get_invoice_net(sales, 'LOCAL_SALE')
                local_sales_refunds_invoice_amount_net = TaxRecordService.get_invoice_net(refunds, 'LOCAL_SALE')
                local_sales_total_invoice_amount_net = CalcService.get_sum(local_sales_sales_invoice_amount_net, local_sales_refunds_invoice_amount_net)

                local_sales_sales_invoice_amount_vat = TaxRecordService.get_invoice_vat(sales, 'LOCAL_SALE')
                local_sales_refunds_invoice_amount_vat = TaxRecordService.get_invoice_vat(refunds, 'LOCAL_SALE')
                local_sales_total_invoice_amount_vat = CalcService.get_sum(local_sales_sales_invoice_amount_vat, local_sales_refunds_invoice_amount_vat)

                local_sales_sales_invoice_amount_gross = TaxRecordService.get_invoice_gross(sales, 'LOCAL_SALE')
                local_sales_refunds_invoice_amount_gross = TaxRecordService.get_invoice_gross(refunds, 'LOCAL_SALE')
                local_sales_total_invoice_amount_gross = CalcService.get_sum(local_sales_sales_invoice_amount_gross, local_sales_refunds_invoice_amount_gross)


                # LOCAL SALES REVERSE CHARGE
                local_sale_reverse_charges_sales_invoice_amount_net = TaxRecordService.get_invoice_net(sales, 'LOCAL_SALE_REVERSE_CHARGE')
                local_sale_reverse_charges_refunds_invoice_amount_net = TaxRecordService.get_invoice_net(refunds, 'LOCAL_SALE_REVERSE_CHARGE')
                local_sale_reverse_charges_total_invoice_amount_net = CalcService.get_sum(local_sale_reverse_charges_sales_invoice_amount_net, local_sale_reverse_charges_refunds_invoice_amount_net)

                local_sale_reverse_charges_sales_invoice_amount_vat = TaxRecordService.get_invoice_vat(sales, 'LOCAL_SALE_REVERSE_CHARGE')
                local_sale_reverse_charges_refunds_invoice_amount_vat = TaxRecordService.get_invoice_vat(refunds, 'LOCAL_SALE_REVERSE_CHARGE')
                local_sale_reverse_charges_total_invoice_amount_vat = CalcService.get_sum(local_sale_reverse_charges_sales_invoice_amount_vat, local_sale_reverse_charges_refunds_invoice_amount_vat)

                local_sale_reverse_charges_sales_invoice_amount_gross = TaxRecordService.get_invoice_gross(sales, 'LOCAL_SALE_REVERSE_CHARGE')
                local_sale_reverse_charges_refunds_invoice_amount_gross = TaxRecordService.get_invoice_gross(refunds, 'LOCAL_SALE_REVERSE_CHARGE')
                local_sale_reverse_charges_total_invoice_amount_gross = CalcService.get_sum(local_sale_reverse_charges_sales_invoice_amount_gross, local_sale_reverse_charges_refunds_invoice_amount_gross)


                # DISTANCE SALES
                distance_sales_sales_invoice_amount_net = TaxRecordService.get_invoice_net(sales, 'DISTANCE_SALE')
                distance_sales_refunds_invoice_amount_net = TaxRecordService.get_invoice_net(refunds, 'DISTANCE_SALE')
                distance_sales_total_invoice_amount_net = CalcService.get_sum(distance_sales_sales_invoice_amount_net, distance_sales_refunds_invoice_amount_net)

                distance_sales_sales_invoice_amount_vat = TaxRecordService.get_invoice_vat(sales, 'DISTANCE_SALE')
                distance_sales_refunds_invoice_amount_vat = TaxRecordService.get_invoice_vat(refunds, 'DISTANCE_SALE')
                distance_sales_total_invoice_amount_vat = CalcService.get_sum(distance_sales_sales_invoice_amount_vat, distance_sales_refunds_invoice_amount_vat)

                distance_sales_sales_invoice_amount_gross = TaxRecordService.get_invoice_gross(sales, 'DISTANCE_SALE')
                distance_sales_refunds_invoice_amount_gross = TaxRecordService.get_invoice_gross(refunds, 'DISTANCE_SALE')
                distance_sales_total_invoice_amount_gross = CalcService.get_sum(distance_sales_sales_invoice_amount_gross, distance_sales_refunds_invoice_amount_gross)


                # NON TAXABLE DISTANCE SALES
                non_taxable_distance_sales_sales_invoice_amount_net = TaxRecordService.get_invoice_net(sales, 'NON_TAXABLE_DISTANCE_SALE')
                non_taxable_distance_sales_refunds_invoice_amount_net = TaxRecordService.get_invoice_net(refunds, 'NON_TAXABLE_DISTANCE_SALE')
                non_taxable_distance_sales_total_invoice_amount_net = CalcService.get_sum(non_taxable_distance_sales_sales_invoice_amount_net, non_taxable_distance_sales_refunds_invoice_amount_net)

                non_taxable_distance_sales_sales_invoice_amount_vat = TaxRecordService.get_invoice_vat(sales, 'NON_TAXABLE_DISTANCE_SALE')
                non_taxable_distance_sales_refunds_invoice_amount_vat = TaxRecordService.get_invoice_vat(refunds, 'NON_TAXABLE_DISTANCE_SALE')
                non_taxable_distance_sales_total_invoice_amount_vat = CalcService.get_sum(non_taxable_distance_sales_sales_invoice_amount_vat, non_taxable_distance_sales_refunds_invoice_amount_vat)

                non_taxable_distance_sales_sales_invoice_amount_gross = TaxRecordService.get_invoice_gross(sales, 'NON_TAXABLE_DISTANCE_SALE')
                non_taxable_distance_sales_refunds_invoice_amount_gross = TaxRecordService.get_invoice_gross(refunds, 'NON_TAXABLE_DISTANCE_SALE')
                non_taxable_distance_sales_total_invoice_amount_gross = CalcService.get_sum(non_taxable_distance_sales_sales_invoice_amount_gross, non_taxable_distance_sales_refunds_invoice_amount_gross)


                # INTRA COMMUNITY SALES
                intra_community_sales_sales_invoice_amount_net = TaxRecordService.get_invoice_net(sales, 'INTRA_COMMUNITY_SALE')
                intra_community_sales_refunds_invoice_amount_net = TaxRecordService.get_invoice_net(refunds, 'INTRA_COMMUNITY_SALE')
                intra_community_sales_total_invoice_amount_net = CalcService.get_sum(intra_community_sales_sales_invoice_amount_net, intra_community_sales_refunds_invoice_amount_net)


                # EXPORTS
                exports_sales_invoice_amount_net = TaxRecordService.get_invoice_net(sales, 'EXPORT')
                exports_refunds_invoice_amount_net = TaxRecordService.get_invoice_net(refunds, 'EXPORT')
                exports_total_invoice_amount_net = CalcService.get_sum(exports_sales_invoice_amount_net, exports_refunds_invoice_amount_net)


                # INTRA COMMUNITY ACQUISITIONS
                intra_community_acquisitions_acquisitions_invoice_amount_net = TaxRecordService.get_invoice_net(acquisitions, 'INTRA_COMMUNITY_ACQUISITION')
                intra_community_acquisitions_refunds_invoice_amount_net = TaxRecordService.get_invoice_net(refunds, 'INTRA_COMMUNITY_ACQUISITION')
                intra_community_acquisitions_total_invoice_amount_net = CalcService.get_sum(intra_community_acquisitions_acquisitions_invoice_amount_net, intra_community_acquisitions_refunds_invoice_amount_net)

                intra_community_acquisitions_acquisitions_invoice_amount_vat_reverse_charge = TaxRecordService.get_vat_reverse_charge(acquisitions, 'INTRA_COMMUNITY_ACQUISITION')
                intra_community_acquisitions_refunds_invoice_amount_vat_reverse_charge = TaxRecordService.get_vat_reverse_charge(refunds, 'INTRA_COMMUNITY_ACQUISITION')
                intra_community_acquisitions_total_invoice_amount_vat_reverse_charge = CalcService.get_sum(intra_community_acquisitions_acquisitions_invoice_amount_vat_reverse_charge, intra_community_acquisitions_refunds_invoice_amount_vat_reverse_charge)


                # LOCAL ACQUISITIONS
                local_acquisitions_acquisitions_invoice_amount_net = TaxRecordService.get_invoice_net(acquisitions, 'DOMESTIC_ACQUISITION')
                local_acquisitions_refunds_invoice_amount_net = TaxRecordService.get_invoice_net(refunds, 'DOMESTIC_ACQUISITION')
                local_acquisitions_total_invoice_amount_net = CalcService.get_sum(local_acquisitions_acquisitions_invoice_amount_net, local_acquisitions_refunds_invoice_amount_net)

                local_acquisitions_acquisitions_invoice_amount_vat = TaxRecordService.get_invoice_vat(acquisitions, 'DOMESTIC_ACQUISITION')
                local_acquisitions_refunds_invoice_amount_vat = TaxRecordService.get_invoice_vat(refunds, 'DOMESTIC_ACQUISITION')
                local_acquisitions_total_invoice_amount_vat = CalcService.get_sum(local_acquisitions_acquisitions_invoice_amount_vat, local_acquisitions_refunds_invoice_amount_vat)

                local_acquisitions_acquisitions_invoice_amount_gross = TaxRecordService.get_invoice_gross(acquisitions, 'DOMESTIC_ACQUISITION')
                local_acquisitions_refunds_invoice_amount_gross = TaxRecordService.get_invoice_gross(refunds, 'DOMESTIC_ACQUISITION')
                local_acquisitions_total_invoice_amount_gross = CalcService.get_sum(local_acquisitions_acquisitions_invoice_amount_gross, local_acquisitions_refunds_invoice_amount_gross)

                # SUMMARY
                taxable_turnover_amount = CalcService.get_sum(local_sales_total_invoice_amount_net, local_sale_reverse_charges_total_invoice_amount_net, distance_sales_total_invoice_amount_net, intra_community_sales_total_invoice_amount_net)
                payable_vat_amount = CalcService.get_sum(local_sales_total_invoice_amount_vat, distance_sales_total_invoice_amount_vat, local_acquisitions_total_invoice_amount_vat)

                tax_record_data = {
                    'created_by': g.user.id,
                    'seller_firm_id': seller_firm.id,

                    'start_date': start_date,
                    'end_date': end_date,
                    'tax_jurisdiction_code': tax_jurisdiction_code,
                    'currency_code': tax_jurisdiction.currency_code,

                    'vatin_id': vatin.id,

                    'local_sales_sales_invoice_amount_net': local_sales_sales_invoice_amount_net,
                    'local_sales_refunds_invoice_amount_net': local_sales_refunds_invoice_amount_net,
                    'local_sales_total_invoice_amount_net': local_sales_total_invoice_amount_net,
                    'local_sales_sales_invoice_amount_vat': local_sales_sales_invoice_amount_vat,
                    'local_sales_refunds_invoice_amount_vat': local_sales_refunds_invoice_amount_vat,
                    'local_sales_total_invoice_amount_vat': local_sales_total_invoice_amount_vat,
                    'local_sales_sales_invoice_amount_gross': local_sales_sales_invoice_amount_gross,
                    'local_sales_refunds_invoice_amount_gross': local_sales_refunds_invoice_amount_gross,
                    'local_sales_total_invoice_amount_gross': local_sales_total_invoice_amount_gross,

                    'local_sale_reverse_charges_sales_invoice_amount_net': local_sale_reverse_charges_sales_invoice_amount_net,
                    'local_sale_reverse_charges_refunds_invoice_amount_net': local_sale_reverse_charges_refunds_invoice_amount_net,
                    'local_sale_reverse_charges_total_invoice_amount_net': local_sale_reverse_charges_total_invoice_amount_net,
                    'local_sale_reverse_charges_sales_invoice_amount_vat': local_sale_reverse_charges_sales_invoice_amount_vat,
                    'local_sale_reverse_charges_refunds_invoice_amount_vat': local_sale_reverse_charges_refunds_invoice_amount_vat,
                    'local_sale_reverse_charges_total_invoice_amount_vat': local_sale_reverse_charges_total_invoice_amount_vat,
                    'local_sale_reverse_charges_sales_invoice_amount_gross': local_sale_reverse_charges_sales_invoice_amount_gross,
                    'local_sale_reverse_charges_refunds_invoice_amount_gross': local_sale_reverse_charges_refunds_invoice_amount_gross,
                    'local_sale_reverse_charges_total_invoice_amount_gross': local_sale_reverse_charges_total_invoice_amount_gross,

                    'distance_sales_sales_invoice_amount_net': distance_sales_sales_invoice_amount_net,
                    'distance_sales_refunds_invoice_amount_net': distance_sales_refunds_invoice_amount_net,
                    'distance_sales_total_invoice_amount_net': distance_sales_total_invoice_amount_net,
                    'distance_sales_sales_invoice_amount_vat': distance_sales_sales_invoice_amount_vat,
                    'distance_sales_refunds_invoice_amount_vat': distance_sales_refunds_invoice_amount_vat,
                    'distance_sales_total_invoice_amount_vat': distance_sales_total_invoice_amount_vat,
                    'distance_sales_sales_invoice_amount_gross': distance_sales_sales_invoice_amount_gross,
                    'distance_sales_refunds_invoice_amount_gross': distance_sales_refunds_invoice_amount_gross,
                    'distance_sales_total_invoice_amount_gross': distance_sales_total_invoice_amount_gross,

                    'non_taxable_distance_sales_sales_invoice_amount_net': non_taxable_distance_sales_sales_invoice_amount_net,
                    'non_taxable_distance_sales_refunds_invoice_amount_net': non_taxable_distance_sales_refunds_invoice_amount_net,
                    'non_taxable_distance_sales_total_invoice_amount_net': non_taxable_distance_sales_total_invoice_amount_net,
                    'non_taxable_distance_sales_sales_invoice_amount_vat': non_taxable_distance_sales_sales_invoice_amount_vat,
                    'non_taxable_distance_sales_refunds_invoice_amount_vat': non_taxable_distance_sales_refunds_invoice_amount_vat,
                    'non_taxable_distance_sales_total_invoice_amount_vat': non_taxable_distance_sales_total_invoice_amount_vat,
                    'non_taxable_distance_sales_sales_invoice_amount_gross': non_taxable_distance_sales_sales_invoice_amount_gross,
                    'non_taxable_distance_sales_refunds_invoice_amount_gross': non_taxable_distance_sales_refunds_invoice_amount_gross,
                    'non_taxable_distance_sales_total_invoice_amount_gross': non_taxable_distance_sales_total_invoice_amount_gross,

                    'intra_community_sales_sales_invoice_amount_net': intra_community_sales_sales_invoice_amount_net,
                    'intra_community_sales_refunds_invoice_amount_net': intra_community_sales_refunds_invoice_amount_net,
                    'intra_community_sales_total_invoice_amount_net': intra_community_sales_total_invoice_amount_net,

                    'exports_sales_invoice_amount_net': exports_sales_invoice_amount_net,
                    'exports_refunds_invoice_amount_net': exports_refunds_invoice_amount_net,
                    'exports_total_invoice_amount_net': exports_total_invoice_amount_net,

                    'intra_community_acquisitions_acquisitions_invoice_amount_net': intra_community_acquisitions_acquisitions_invoice_amount_net,
                    'intra_community_acquisitions_refunds_invoice_amount_net': intra_community_acquisitions_refunds_invoice_amount_net,
                    'intra_community_acquisitions_total_invoice_amount_net': intra_community_acquisitions_total_invoice_amount_net,
                    'intra_community_acquisitions_acquisitions_invoice_amount_vat_reverse_charge': intra_community_acquisitions_acquisitions_invoice_amount_vat_reverse_charge,
                    'intra_community_acquisitions_refunds_invoice_amount_vat_reverse_charge': intra_community_acquisitions_refunds_invoice_amount_vat_reverse_charge,
                    'intra_community_acquisitions_total_invoice_amount_vat_reverse_charge': intra_community_acquisitions_total_invoice_amount_vat_reverse_charge,

                    'local_acquisitions_acquisitions_invoice_amount_net': local_acquisitions_acquisitions_invoice_amount_net,
                    'local_acquisitions_refunds_invoice_amount_net': local_acquisitions_refunds_invoice_amount_net,
                    'local_acquisitions_total_invoice_amount_net': local_acquisitions_total_invoice_amount_net,
                    'local_acquisitions_acquisitions_invoice_amount_vat': local_acquisitions_acquisitions_invoice_amount_vat,
                    'local_acquisitions_refunds_invoice_amount_vat': local_acquisitions_refunds_invoice_amount_vat,
                    'local_acquisitions_total_invoice_amount_vat': local_acquisitions_total_invoice_amount_vat,
                    'local_acquisitions_acquisitions_invoice_amount_gross': local_acquisitions_acquisitions_invoice_amount_gross,
                    'local_acquisitions_refunds_invoice_amount_gross': local_acquisitions_refunds_invoice_amount_gross,
                    'local_acquisitions_total_invoice_amount_gross': local_acquisitions_total_invoice_amount_gross,

                    'taxable_turnover_amount': taxable_turnover_amount,
                    'payable_vat_amount': payable_vat_amount
                }

                try:
                    tax_record = TaxRecordService.create(tax_record_data)
                except:
                    db.session.rollback()
                    raise

                try:
                    TaxRecordService.extend_transactions(tax_record, transactions)
                except:
                    db.session.rollback()
                    raise

                return tax_record

        else:
            raise NotFound('A seller firm with the id "{}" does not exist.'.format(seller_firm_public_id))



    @staticmethod
    def get_invoice_net(transactions: List[Transaction], tax_treatment_code: str):
        return sum([transaction.invoice_amount_net for transaction in transactions if transaction.tax_treatment_code == tax_treatment_code]) if not len(transactions) == 0 else 0

    @staticmethod
    def get_invoice_vat(transactions: List[Transaction], tax_treatment_code: str):
        return sum([transaction.invoice_amount_vat for transaction in transactions if transaction.tax_treatment_code == tax_treatment_code]) if not len(transactions) == 0 else 0

    @staticmethod
    def get_invoice_gross(transactions: List[Transaction], tax_treatment_code: str):
        return sum([transaction.invoice_amount_gross for transaction in transactions if transaction.tax_treatment_code == tax_treatment_code]) if not len(transactions) == 0 else 0

    @staticmethod
    def get_vat_reverse_charge(transactions: List[Transaction], tax_treatment_code: str):
        return sum([transaction.invoice_amount_vat_reverse_charge for transaction in transactions if transaction.tax_treatment_code == tax_treatment_code]) if not len(transactions) == 0 else 0







    @staticmethod
    def create(tax_record_data: TaxRecordInterface) -> TaxRecord:


        new_tax_record = TaxRecord(
            created_by = tax_record_data.get('created_by'),
            seller_firm_id = tax_record_data.get('seller_firm_id'),

            start_date = tax_record_data.get('start_date'),
            end_date = tax_record_data.get('end_date'),
            tax_jurisdiction_code = tax_record_data.get('tax_jurisdiction_code'),
            currency_code=tax_record_data.get('currency_code'),

            vatin_id=tax_record_data.get('vatin_id'),

            local_sales_sales_invoice_amount_net = tax_record_data.get('local_sales_sales_invoice_amount_net'),
            local_sales_refunds_invoice_amount_net = tax_record_data.get('local_sales_refunds_invoice_amount_net'),
            local_sales_total_invoice_amount_net = tax_record_data.get('local_sales_total_invoice_amount_net'),
            local_sales_sales_invoice_amount_vat = tax_record_data.get('local_sales_sales_invoice_amount_vat'),
            local_sales_refunds_invoice_amount_vat = tax_record_data.get('local_sales_refunds_invoice_amount_vat'),
            local_sales_total_invoice_amount_vat = tax_record_data.get('local_sales_total_invoice_amount_vat'),
            local_sales_sales_invoice_amount_gross = tax_record_data.get('local_sales_sales_invoice_amount_gross'),
            local_sales_refunds_invoice_amount_gross = tax_record_data.get('local_sales_refunds_invoice_amount_gross'),
            local_sales_total_invoice_amount_gross = tax_record_data.get('local_sales_total_invoice_amount_gross'),

            local_sale_reverse_charges_sales_invoice_amount_net = tax_record_data.get('local_sale_reverse_charges_sales_invoice_amount_net'),
            local_sale_reverse_charges_refunds_invoice_amount_net = tax_record_data.get('local_sale_reverse_charges_refunds_invoice_amount_net'),
            local_sale_reverse_charges_total_invoice_amount_net = tax_record_data.get('local_sale_reverse_charges_total_invoice_amount_net'),
            local_sale_reverse_charges_sales_invoice_amount_vat = tax_record_data.get('local_sale_reverse_charges_sales_invoice_amount_vat'),
            local_sale_reverse_charges_refunds_invoice_amount_vat = tax_record_data.get('local_sale_reverse_charges_refunds_invoice_amount_vat'),
            local_sale_reverse_charges_total_invoice_amount_vat = tax_record_data.get('local_sale_reverse_charges_total_invoice_amount_vat'),
            local_sale_reverse_charges_sales_invoice_amount_gross = tax_record_data.get('local_sale_reverse_charges_sales_invoice_amount_gross'),
            local_sale_reverse_charges_refunds_invoice_amount_gross = tax_record_data.get('local_sale_reverse_charges_refunds_invoice_amount_gross'),
            local_sale_reverse_charges_total_invoice_amount_gross = tax_record_data.get('local_sale_reverse_charges_total_invoice_amount_gross'),

            distance_sales_sales_invoice_amount_net = tax_record_data.get('distance_sales_sales_invoice_amount_net'),
            distance_sales_refunds_invoice_amount_net = tax_record_data.get('distance_sales_refunds_invoice_amount_net'),
            distance_sales_total_invoice_amount_net = tax_record_data.get('distance_sales_total_invoice_amount_net'),
            distance_sales_sales_invoice_amount_vat = tax_record_data.get('distance_sales_sales_invoice_amount_vat'),
            distance_sales_refunds_invoice_amount_vat = tax_record_data.get('distance_sales_refunds_invoice_amount_vat'),
            distance_sales_total_invoice_amount_vat = tax_record_data.get('distance_sales_total_invoice_amount_vat'),
            distance_sales_sales_invoice_amount_gross = tax_record_data.get('distance_sales_sales_invoice_amount_gross'),
            distance_sales_refunds_invoice_amount_gross = tax_record_data.get('distance_sales_refunds_invoice_amount_gross'),
            distance_sales_total_invoice_amount_gross = tax_record_data.get('distance_sales_total_invoice_amount_gross'),

            non_taxable_distance_sales_sales_invoice_amount_net = tax_record_data.get('non_taxable_distance_sales_sales_invoice_amount_net'),
            non_taxable_distance_sales_refunds_invoice_amount_net = tax_record_data.get('non_taxable_distance_sales_refunds_invoice_amount_net'),
            non_taxable_distance_sales_total_invoice_amount_net = tax_record_data.get('non_taxable_distance_sales_total_invoice_amount_net'),
            non_taxable_distance_sales_sales_invoice_amount_vat = tax_record_data.get('non_taxable_distance_sales_sales_invoice_amount_vat'),
            non_taxable_distance_sales_refunds_invoice_amount_vat = tax_record_data.get('non_taxable_distance_sales_refunds_invoice_amount_vat'),
            non_taxable_distance_sales_total_invoice_amount_vat = tax_record_data.get('non_taxable_distance_sales_total_invoice_amount_vat'),
            non_taxable_distance_sales_sales_invoice_amount_gross = tax_record_data.get('non_taxable_distance_sales_sales_invoice_amount_gross'),
            non_taxable_distance_sales_refunds_invoice_amount_gross = tax_record_data.get('non_taxable_distance_sales_refunds_invoice_amount_gross'),
            non_taxable_distance_sales_total_invoice_amount_gross = tax_record_data.get('non_taxable_distance_sales_total_invoice_amount_gross'),

            intra_community_sales_sales_invoice_amount_net = tax_record_data.get('intra_community_sales_sales_invoice_amount_net'),
            intra_community_sales_refunds_invoice_amount_net = tax_record_data.get('intra_community_sales_refunds_invoice_amount_net'),
            intra_community_sales_total_invoice_amount_net = tax_record_data.get('intra_community_sales_total_invoice_amount_net'),

            exports_sales_invoice_amount_net = tax_record_data.get('exports_sales_invoice_amount_net'),
            exports_refunds_invoice_amount_net = tax_record_data.get('exports_refunds_invoice_amount_net'),
            exports_total_invoice_amount_net = tax_record_data.get('exports_total_invoice_amount_net'),

            intra_community_acquisitions_acquisitions_invoice_amount_net = tax_record_data.get('intra_community_acquisitions_acquisitions_invoice_amount_net'),
            intra_community_acquisitions_refunds_invoice_amount_net = tax_record_data.get('intra_community_acquisitions_refunds_invoice_amount_net'),
            intra_community_acquisitions_total_invoice_amount_net = tax_record_data.get('intra_community_acquisitions_total_invoice_amount_net'),
            intra_community_acquisitions_acquisitions_invoice_amount_vat_reverse_charge = tax_record_data.get('intra_community_acquisitions_acquisitions_invoice_amount_vat_reverse_charge'),
            intra_community_acquisitions_refunds_invoice_amount_vat_reverse_charge = tax_record_data.get('intra_community_acquisitions_refunds_invoice_amount_vat_reverse_charge'),
            intra_community_acquisitions_total_invoice_amount_vat_reverse_charge = tax_record_data.get('intra_community_acquisitions_total_invoice_amount_vat_reverse_charge'),

            local_acquisitions_acquisitions_invoice_amount_net = tax_record_data.get('local_acquisitions_acquisitions_invoice_amount_net'),
            local_acquisitions_refunds_invoice_amount_net = tax_record_data.get('local_acquisitions_refunds_invoice_amount_net'),
            local_acquisitions_total_invoice_amount_net = tax_record_data.get('local_acquisitions_total_invoice_amount_net'),
            local_acquisitions_acquisitions_invoice_amount_vat = tax_record_data.get('local_acquisitions_acquisitions_invoice_amount_vat'),
            local_acquisitions_refunds_invoice_amount_vat = tax_record_data.get('local_acquisitions_refunds_invoice_amount_vat'),
            local_acquisitions_total_invoice_amount_vat = tax_record_data.get('local_acquisitions_total_invoice_amount_vat'),
            local_acquisitions_acquisitions_invoice_amount_gross = tax_record_data.get('local_acquisitions_acquisitions_invoice_amount_gross'),
            local_acquisitions_refunds_invoice_amount_gross = tax_record_data.get('local_acquisitions_refunds_invoice_amount_gross'),
            local_acquisitions_total_invoice_amount_gross = tax_record_data.get('local_acquisitions_total_invoice_amount_gross'),

            taxable_turnover_amount = tax_record_data.get('taxable_turnover_amount'),
            payable_vat_amount = tax_record_data.get('payable_vat_amount')
        )

        db.session.add(new_tax_record)
        db.session.commit()

        return new_tax_record


    @staticmethod
    def extend_transactions(tax_record: TaxRecord, transactions: List[Transaction]):
        tax_record.transactions.extend(transactions)
        db.session.commit()










    # @staticmethod
    # def get_df_list(tax_record_dict: TaxRecordDictInterface) -> List[Union[pd.DataFrame, str]]:
    #     tab_names = ['LOCAL_SALES', 'LOCAL_SALES_REVERSE_CHARGE', 'DISTANCE_SALES', 'NON_TAXABLE_DISTANCE_SALES', 'INTRA_COMMUNITY_SALES', 'EXPORTS', 'DOMESTIC_ACQUISITIONS', 'INTRA_COMMUNITY_ACQUISITIONS']
    #     #'SUMMARY',
    #     df_local_sales = pd.Dataframe(tax_record_dict.get('LOCAL_SALES'))
    #     df_local_sales_reverse_charge = pd.Dataframe(tax_record_dict.get('LOCAL_SALES_REVERSE_CHARGE'))
    #     df_distance_sales = pd.Dataframe(tax_record_dict.get('DISTANCE_SALES'))
    #     df_non_taxable_distance_sales = pd.Dataframe(tax_record_dict.get('NON_TAXABLE_DISTANCE_SALES'))
    #     df_intra_community_sales = pd.Dataframe(tax_record_dict.get('INTRA_COMMUNITY_SALES'))
    #     df_exports = pd.Dataframe(tax_record_dict.get('EXPORTS'))
    #     df_domestic_acquisitions = pd.Dataframe(tax_record_dict.get('DOMESTIC_ACQUISITIONS'))
    #     df_intra_community_acquisitions = pd.Dataframe(tax_record_dict.get('INTRA_COMMUNITY_ACQUISITIONS'))
    #     #df_summary = TaxRecordService.calculate_front_page(df_local_sales, df_local_sales_reverse_charge, df_distance_sales, df_non_taxable_distance_sales, df_intra_community_sales, df_exports, df_domestic_acquisitions, df_intra_community_acquisitions)

    #     df_list = [df_local_sales, df_local_sales_reverse_charge, df_distance_sales, df_non_taxable_distance_sales, df_intra_community_sales, df_exports, df_domestic_acquisitions, df_intra_community_acquisitions]
    #     #df_summary,

    #     # !!! evtl. dies für summary :
    #     # ####

    #     #             https: // stackoverflow.com/questions/18423298/easy-way-to-fill-in-an-excel-file-with-python



    #     # ####


    #     return tab_names, df_list



    # # celery task on this level
    # @staticmethod
    # def save_as_file(start_date_str: str, end_date_str: str, seller_firm_public_id: UUID, basepath: str, user_id: int, tax_jurisdiction_code: str) -> BinaryIO:
    #     from ..transaction.service import TransactionService

    #     transactions = TransactionService.get_by_validity_public_id(start_date_str, end_date_str, seller_firm_public_id, tax_jurisdiction_code)

    #     tax_record_dict = TaxRecordService.get_tax_record_dict_from_transactions(transactions)

    #     # list of dataframes and sheet names
    #     tab_names, df_list = TaxRecordService.get_df_list(tax_record_dict)
    #     filename=TaxRecordService.create_filename(seller_firm_public_id, start_date_str, end_date_str)
    #     os.makedirs(basepath, exist_ok=True)
    #     file_path=os.path.join(basepath_in, filename)


    #     # run function
    #     tax_record_file= TaxRecordService.write_dfs_to_xlsx(dfs, sheets, file_path)


    #     TaxRecordService.create(start_date_str, end_date_str, seller_firm_public_id, filename, user_id)




    #     # @staticmethod
    #     # !!! def calculate_front_page(df_local_sales: pd.DataFrame, df_local_sales_reverse_charge: pd.DataFrame, df_distance_sales: pd.DataFrame, df_non_taxable_distance_sales: pd.DataFrame, df_intra_community_sales: pd.DataFrame, df_exports: pd.DataFrame, df_domestic_acquisitions: pd.DataFrame, df_intra_community_acquisitions: pd.DataFrame) -> pd.DataFrame:

    #     #     ### something happens here


    #     #     return df_summary


    #     @staticmethod
    #     def create_filename(seller_firm_public_id: UUID, start_date_str: str, end_date_str: str) -> str:
    #         today_as_str = str(date.today().strftime('%Y%m%d'))
    #         seller_firm = Seller.query.filter(public_id = seller_firm_public_id).first()
    #         if seller_firm.accounting_firm_client_id:
    #             filename = '{}_{}_EXPORT_{}_{}.xlsx'.format(today_as_str, seller_firm.accounting_firm_client_id, start_date_str, end_date_str)
    #         else:
    #             filename = '{}_{}_EXPORT_{}_{}.xlsx'.format(today_as_str, seller_firm_public_id, start_date_str, end_date_str)

    #         return filename



    #     @staticmethod
    #     def write_dfs_to_xlsx(df_list, tab_names, file_path):
    #         writer=pd.ExcelWriter(path=file_path, engine='xlsxwriter')
    #         for dataframe, sheet in zip(df_list, tab_names):
    #             dataframe.to_excel(writer, sheet_name=sheet, startrow=0, startcol=0)
    #             writer.save()






    # @staticmethod
    # def append_to_tax_record_dict(tax_record_dict: Dict, t_treatment_code: str, t_type_dict: Dict):
    #     if t_treatment_code == 'LOCAL_SALE':
    #         t_treatment_list: List[Dict] = tax_record_dict.get('LOCAL_SALES')

    #     elif t_treatment_code == 'LOCAL_SALE_REVERSE_CHARGE':
    #         t_treatment_list: List[Dict] = tax_record_dict.get('LOCAL_SALE_REVERSE_CHARGES')

    #     elif t_treatment_code == 'DISTANCE_SALE':
    #         t_treatment_list: List[Dict] = tax_record_dict.get('DISTANCE_SALES')

    #     elif t_treatment_code == 'NON_TAXABLE_DISTANCE_SALE':
    #         t_treatment_list: List[Dict] = tax_record_dict.get('NON_TAXABLE_DISTANCE_SALES')

    #     elif t_treatment_code == 'INTRA_COMMUNITY_SALE':
    #         t_treatment_list: List[Dict] = tax_record_dict.get('INTRA_COMMUNITY_SALES')

    #     elif t_treatment_code == 'EXPORT':
    #         t_treatment_list: List[Dict] = tax_record_dict.get('EXPORTS')

    #     elif t_treatment_code == 'DOMESTIC_ACQUISITION':
    #         t_treatment_list: List[Dict] = tax_record_dict.get('DOMESTIC_ACQUISITIONS')

    #     elif t_treatment_code == 'INTRA_COMMUNITY_ACQUISITION':
    #         t_treatment_list: List[Dict] = tax_record_dict.get('INTRA_COMMUNITY_ACQUISITIONS')


    #     else:
    #         raise InternalServerError

    #     t_treatment_list.append(t_type_dict)



    # @staticmethod
    # def create_t_type_dict(t_treatment_code: str, tax_record_base_dict: Dict, transaction_input: TransactionInput, t: Transaction) -> Dict:
    #     if t_treatment_code == 'LOCAL_SALE':
    #         t_type_dict=tax_record_base_dict

    #     elif t_treatment_code == 'LOCAL_SALE_REVERSE_CHARGE':
    #         add_local_sales_reverse_charge = {
    #             'VAT_RATE_REVERSE_CHARGE': t.vat_rate_reverse_charge,
    #             'INVOICE_AMOUNT_VAT_REVERSE_CHARGE': t.invoice_amount_vat_reverse_charge
    #         }

    #         t_type_dict={**tax_record_base_dict, **add_local_sales_reverse_charge}


    #     elif t_treatment_code == 'DISTANCE_SALE':
    #         t_type_dict = tax_record_base_dict

    #     elif t_treatment_code == 'NON_TAXABLE_DISTANCE_SALE':
    #         t_type_dict = tax_record_base_dict

    #     elif t_treatment_code == 'INTRA_COMMUNITY_SALE':
    #         t_type_dict = tax_record_base_dict

    #     elif t_treatment_code == 'EXPORT':
    #         t_type_dict = tax_record_base_dict

    #     elif t_treatment_code == 'DOMESTIC_ACQUISITION':
    #         t_type_dict = tax_record_base_dict

    #     elif t_treatment_code == 'INTRA_COMMUNITY_ACQUISITION':
    #         t_type_dict = tax_record_base_dict


    #     else:
    #         raise UnprocessableEntity('Transaction type unknown.')

    #     return t_type_dict




    # @staticmethod
    # def get_tax_record_dict_from_transactions(transactions: Transaction) -> TaxRecordDictInterface:
    #     from ..tax.vatin.service import VATINService
    #     from ..tax.vatin import VATIN
    #     from ..user.service_parent import UserService



    #     local_sales = local_sales_reverse_charge = distance_sales = non_taxable_distance_sales = intra_community_sales = exports = domestic_acquisitions = intra_community_acquisitions = []
    #     t_treatment_list=[]

    #     tax_record_dict = {
    #         'LOCAL_SALES': local_sales,
    #         'LOCAL_SALE_REVERSE_CHARGES': local_sales_reverse_charge,
    #         'DISTANCE_SALES': distance_sales,
    #         'NON_TAXABLE_DISTANCE_SALES': non_taxable_distance_sales,
    #         'INTRA_COMMUNITY_SALES': intra_community_sales,
    #         'EXPORTS': exports,
    #         'DOMESTIC_ACQUISITIONS': domestic_acquisitions,
    #         'INTRA_COMMUNITY_ACQUISITIONS': intra_community_acquisitions
    #     }


    #     for t in transactions:
    #         seller_firm = SellerFirm.query.filter(id = t.account.seller_firm_id).first()
    #         t_treatment_code = t.tax_treatment
    #         transaction_input = TransactionInput.query.filter_by(transaction_id = t.id).first()
    #         arrival_seller_vatin = VATINService.get_by_id(t.arrival_seller_vatin_id)
    #         departure_seller_vatin = VATINService.get_by_id(t.departure_seller_vatin_id)
    #         seller_vatin = VATINService.get_by_id(t.seller_vatin_id)
    #         customer_firm_vatin=VATINService.get_by_id(t.customer_firm_vatin_id)

    #         info_notifications: List[TransactionNotification] = NotificationService.get_by_transaction_input_id_status(transaction_input.id, 'info')
    #         warning_notifications: List[TransactionNotification] = NotificationService.get_by_transaction_input_id_status(transaction_input.id, 'warning')


    #         tax_record_base_dict = {

    #             'SELLER_FIRM_ID': seller_firm.id,
    #             'SELLER_FIRM_NAME': seller_firm.name,
    #             'SELLER_FIRM_ADDRESS': seller_firm.address,
    #             'SELLER_FIRM_ESTABLISHMENT_COUNTRY': seller_firm.establishment_country_code,

    #             'CREATED_BY': UserService.get_by_id(id=transaction_input.created_by).name,
    #             'ORIGINAL_FILENAME': transaction_input.original_filename,

    #             'ACCOUNT_GIVEN_ID': transaction_input.account_given_id,
    #             'CHANNEL_CODE': transaction_input.channel_code,
    #             'MARKETPLACE': transaction_input.marketplace,
    #             'TRANSACTION_TYPE': t.transaction_type,

    #             'TRANSACTION_GIVEN_ID': transaction_input.given_id,
    #             'ACTIVITY_ID': transaction_input.activity_id,

    #             'AMAZON_VAT_CALCULATION_SERVICE': t.amazon_vat_calculation_service,
    #             'CUSTOMER_RELATIONSHIP': t.customer_relationship,
    #             'CUSTOMER_RELATIONSHIP_CHECKED': t.customer_relationship_checked,

    #             'TAX_JURISDICTION_CODE': t.tax_jurisdiction_code,

    #             'TAX_TREATMENT_CODE': t.tax_treatment_code,

    #             'TAX_DATE': t.tax_date,
    #             'TAX_CALCULATION_DATE': t.tax_calculation_date,
    #             'SHIPMENT_DATE': transaction_input.shipment_date,

    #             'ITEM_SKU': transaction_input.item_sku,
    #             'ITEM_NAME': transaction_input.item_name,
    #             'ITEM_QUANTITY': transaction_input.item_quantity,

    #             'ITEM_TAX_CODE': t.item_tax_code_code,
    #             'ITEM_TAX_RATE_TYPE': t.item_tax_rate_type_code,

    #             'ITEM_PRICE_NET': t.item_price_net,
    #             'ITEM_PRICE_DISCOUNT_NET': t.item_price_discount_net,
    #             'ITEM_PRICE_TOTAL_NET': t.item_price_total_net,

    #             'SHIPMENT_PRICE_NET': t.shipment_price_net,
    #             'SHIPMENT_PRICE_DISCOUNT_NET': t.shipment_price_discount_net,
    #             'SHIPMENT_PRICE_TOTAL_NET': t.shipment_price_total_net,

    #             'GIFT_WRAP_PRICE_NET': t.gift_wrap_price_net,
    #             'GIFT_WRAP_PRICE_DISCOUNT_NET': t.gift_wrap_price_discount_net,
    #             'GIFT_WRAP_PRICE_TOTAL_NET': t.gift_wrap_price_total_net,

    #             'ITEM_PRICE_VAT_RATE': t.item_price_vat_rate,
    #             'ITEM_PRICE_VAT': t.item_price_vat,
    #             'ITEM_PRICE_DISCOUNT_VAT': t.item_price_discount_vat,
    #             'ITEM_PRICE_TOTAL_VAT': t.item_price_total_vat,

    #             'SHIPMENT_PRICE_VAT_RATE': t.shipment_price_vat_rate,
    #             'SHIPMENT_PRICE_VAT': t.shipment_price_vat,
    #             'SHIPMENT_PRICE_DISCOUNT_VAT': t.shipment_price_discount_vat,
    #             'SHIPMENT_PRICE_TOTAL_VAT': t.shipment_price_total_vat,

    #             'GIFT_WRAP_PRICE_VAT_RATE': t.gift_wrap_price_vat_rate,
    #             'GIFT_WRAP_PRICE_VAT': t.gift_wrap_price_vat,
    #             'GIFT_WRAP_PRICE_DISCOUNT_VAT': t.gift_wrap_price_discount_vat,
    #             'GIFT_WRAP_PRICE_TOTAL_VAT': t.gift_wrap_price_total_vat,

    #             'TOTAL_VALUE_NET': t.total_value_net,
    #             'TOTAL_VALUE_VAT': t.total_value_vat,
    #             'TOTAL_VALUE_GROSS': t.total_value_gross,

    #             'ITEM_PRICE_GROSS': transaction_input.item_price_gross,
    #             'ITEM_PRICE_DISCOUNT_GROSS': transaction_input.item_price_discount_gross,
    #             'ITEM_PRICE_TOTAL_GROSS': transaction_input.item_price_total_gross,

    #             'SHIPMENT_PRICE_GROSS': transaction_input.shipment_price_gross,
    #             'SHIPMENT_PRICE_DISCOUNT_GROSS': transaction_input.shipment_price_discount_gross,
    #             'SHIPMENT_PRICE_TOTAL_GROSS': transaction_input.shipment_price_total_gross,

    #             'GIFT_WRAP_PRICE_GROSS': transaction_input.gift_wrap_price_gross,
    #             'GIFT_WRAP_PRICE_DISCOUNT_GROSS': transaction_input.gift_wrap_price_discount_net,
    #             'GIFT_WRAP_PRICE_TOTAL_GROSS': transaction_input.gift_wrap_price_total_gross,

    #             'DEPARTURE_CITY': transaction_input.departure_city,
    #             'DEPARTURE_COUNTRY': transaction_input.departure_country_code,
    #             'DEPARTURE_POSTAL_CODE': transaction_input.departure_postal_code,

    #             'ARRIVAL_CITY': transaction_input.departure_city,
    #             'ARRIVAL_COUNTRY': transaction_input.departure_country_code,
    #             'ARRIVAL_POSTAL_CODE': transaction_input.departure_postal_code,

    #             'DEPARTURE_SELLER_VAT_NUMBER_COUNTRY': departure_seller_vatin.country_code if isinstance(departure_seller_vatin, VATIN) else None,
    #             'DEPARTURE_SELLER_VAT_NUMBER': departure_seller_vatin.number if isinstance(departure_seller_vatin, VATIN) else None,
    #             'DEPARTURE_SELLER_VAT_VALID': departure_seller_vatin.valid if isinstance(departure_seller_vatin, VATIN) else None,
    #             'DEPARTURE_SELLER_VAT_CHECKED_DATE': departure_seller_vatin.created_on if isinstance(departure_seller_vatin, VATIN) else None,

    #             'ARRIVAL_SELLER_VAT_NUMBER_COUNTRY': arrival_seller_vatin.country_code if isinstance(arrival_seller_vatin, VATIN) else None,
    #             'ARRIVAL_SELLER_VAT_NUMBER': arrival_seller_vatin.number if isinstance(arrival_seller_vatin, VATIN) else None,
    #             'ARRIVAL_SELLER_VAT_VALID': arrival_seller_vatin.valid if isinstance(arrival_seller_vatin, VATIN) else None,
    #             'ARRIVAL_SELLER_VAT_CHECKED_DATE': arrival_seller_vatin.created_on if isinstance(arrival_seller_vatin, VATIN) else None,

    #             'SELLER_VAT_NUMBER_COUNTRY': arrival_seller_vatin.country_code if isinstance(arrival_seller_vatin, VATIN) else None,
    #             'SELLER_VAT_NUMBER': arrival_seller_vatin.number if isinstance(arrival_seller_vatin, VATIN) else None,
    #             'SELLER_VAT_VALID': arrival_seller_vatin.valid if isinstance(arrival_seller_vatin, VATIN) else None,
    #             'SELLER_VAT_CHECKED_DATE': arrival_seller_vatin.created_on if isinstance(arrival_seller_vatin, VATIN) else None,

    #             'CUSTOMER_FIRM_VAT_NUMBER_COUNTRY': customer_firm_vatin.country_code if isinstance(customer_firm_vatin, VATIN) else None,
    #             'CUSTOMER_FIRM_VAT_NUMBER': customer_firm_vatin.number if isinstance(customer_firm_vatin, VATIN) else None,
    #             'CUSTOMER_FIRM_VAT_VALID': customer_firm_vatin.valid if isinstance(customer_firm_vatin, VATIN) else None,
    #             'CUSTOMER_FIRM_VAT_CHECKED_DATE': customer_firm_vatin.created_on if isinstance(customer_firm_vatin, VATIN) else None,

    #             'INVOICE_AMOUNT_NET': t.invoice_amount_net,
    #             'INVOICE_AMOUNT_VAT': t.invoice_amount_vat,
    #             'INVOICE_AMOUNT_GROSS': t.invoice_amount_gross,

    #             'INVOICE_CURRENCY': t.invoice_currency_code,
    #             'INVOICE_EXCHANGE_RATE_DATE': t.invoice_exchange_rate_date,
    #             'INVOICE_EXCHANGE_RATE': t.invoice_exchange_rate,
    #             'INVOICE_NUMBER': transaction_input.invoice_number,
    #             'INVOICE_URL': transaction_input.invoice_url,

    #             'ARRIVAL_ADDRESS': transaction_input.arrival_address,
    #             'SUPPLIER_NAME': transaction_input.supplier_name,
    #             'SUPPLIER_VAT_NUMBER': transaction_input.supplier_vat_number
    #         }

    #         t_type_dict = TaxRecordService.create_t_type_dict(t_treatment_code, tax_record_base_dict, transaction_input, t)
    #         TaxRecordService.append_to_tax_record_dict(tax_record_dict, t_treatment_code, t_type_dict)

    #     return tax_record_dict
