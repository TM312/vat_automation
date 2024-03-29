import pandas as pd
from datetime import date, timedelta
from flask import g, current_app, send_from_directory
from typing import List, BinaryIO, Dict, Union
from uuid import UUID

from app.extensions import db

from werkzeug.exceptions import UnprocessableEntity, InternalServerError, Unauthorized, NotFound, ExpectationFailed

from .interface import TaxRecordDictInterface, TaxRecordInterface
from . import TaxRecord
from .schema import TaxRecordSubSchema

from app.namespaces.utils.service import HelperService, NotificationService, InputService
from app.namespaces.utils import TransactionNotification
from app.namespaces.transaction import Transaction
from app.namespaces.transaction.service import TransactionService, TransactionExportService
from app.namespaces.transaction_input import TransactionInput
#from app.namespaces.transaction_input.service import TransactionInputService

from app.extensions.socketio.emitters import SocketService


class TaxRecordService:
    @staticmethod
    def get_all() -> List[TaxRecord]:
        tax_records = TaxRecord.query.all()
        return tax_records

    @staticmethod
    def get_by_public_id(tax_record_public_id: str) -> TaxRecord:
        return TaxRecord.query.filter_by(public_id=tax_record_public_id).first()

    @staticmethod
    def create_for_bond_store_ltd(seller_firm_public_id: str, parameters: List) -> TaxRecord:
        from app.namespaces.user.seller.service import SellerService
        james = SellerService.get_by_email('james.b@mi6-mail.com')
        return TaxRecordService.create_by_seller_firm_public_id(seller_firm_public_id, james.id, tax_record_data_raw=parameters)


    @staticmethod
    def get_by_seller_firm_tax_jurisdiction_validity(seller_firm_id: int, tax_jurisdiction_code: str, start_date: date, end_date: date) -> TaxRecord:
        return TaxRecord.query.filter(
            TaxRecord.seller_firm_id == seller_firm_id,
            TaxRecord.tax_jurisdiction_code == tax_jurisdiction_code,
            TaxRecord.start_date == start_date,
            TaxRecord.end_date == end_date
        ).first()

    @staticmethod
    def get_all_by_seller_firm_public_id(seller_firm_public_id: str) -> List[TaxRecord]:
        from app.namespaces.business.seller_firm.service import SellerFirmService
        seller_firm_id = SellerFirmService.get_seller_firm_id(seller_firm_public_id=seller_firm_public_id)
        if isinstance(seller_firm_id, int):
            return TaxRecord.query.filter_by(seller_firm_id=seller_firm_id).all()

    @staticmethod
    def delete_by_public_id(tax_record_public_id: str):
        tax_record = TaxRecordService.get_by_public_id(tax_record_public_id)
        if tax_record:
            db.session.delete(tax_record)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Transaction input (public_id: {}) has been successfully deleted.'.format(tax_record_public_id)
            }
            return response_object
        else:
            raise NotFound('This transaction input does not exist.')



    @staticmethod
    def retrieve_input_vars(object_type: str, seller_firm_public_id: str, tax_record_data_raw: Dict):
        from app.namespaces.business.seller_firm.service import SellerFirmService
        from app.namespaces.business.seller_firm import SellerFirm
        from app.namespaces.tax.vatin.service import VATINService
        from app.namespaces.tax.vatin import VATIN
        from app.namespaces.country.service import CountryService


        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if not isinstance(seller_firm, SellerFirm):
            SocketService.emit_status_error_no_seller_firm(object_type)
            return False

        try:
            start_date = HelperService.get_date_from_str(tax_record_data_raw.get('start_date'), '%Y-%m-%d')
        except:
            raise ExpectationFailed('start_date')

        try:
            end_date = HelperService.get_date_from_str(tax_record_data_raw.get('end_date'), '%Y-%m-%d')
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'end date', 0)
            return False

        try:
            tax_jurisdiction_code = tax_record_data_raw.get('tax_jurisdiction_code')
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'tax jurisdiction', 0)
            return False


        try:
            tax_jurisdiction = CountryService.get_by_code(tax_jurisdiction_code)
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'tax jurisdiction', 0)
            return False

        try:
            vatin = VATINService.get_by_country_code_seller_firm_id(tax_jurisdiction_code, seller_firm.id)
        except:
            SocketService.emit_status_error_unidentifiable_object(object_type, 'tax jurisdiction', 0)
            return False

        if not isinstance(vatin, VATIN):
            raise NotFound('A VATIN for the indicated tax jurisdiction does not exist for this seller firm.')

        transactions = TransactionService.get_by_validity_tax_jurisdiction_seller_firm(start_date, end_date, seller_firm.id, tax_jurisdiction_code)
        if len(transactions) == 0:
            message = 'There are no transactions by this seller for this period and tax jurisdiction.'
            raise ExpectationFailed(message)

        return (
            seller_firm,
            start_date,
            end_date,
            tax_jurisdiction,
            vatin,
            transactions
        )



    @staticmethod
    def get_taxable_turnover_amount_365d(seller_firm_id: int, tax_jurisdiction_code: str, end_date: date, transactions: List[Transaction]) -> float:

        #365 days before end
        start_date = end_date - timedelta(days=365)

        sales, refunds, _, movements = TransactionExportService.separate_transactions_by_type(transactions)

        (
            __local_sales_sales_net__, __local_sales_refunds_net__,
            local_sales_total_net, #this is the only variable of interest
            __local_sales_sales_vat__, __local_sales_refunds_vat__, __local_sales_total_vat__, __local_sales_sales_gross__, __local_sales_refunds_gross__, __local_sales_total_gross__
        ) = TaxRecordService.get_amounts_local_sales(sales, refunds)

        (
            __local_sale_reverse_charges_sales_net__, __local_sale_reverse_charges_refunds_net__,
            local_sale_reverse_charges_total_net, #this is the only variable of interest
            __local_sale_reverse_charges_sales_vat__, __local_sale_reverse_charges_refunds_vat__, __local_sale_reverse_charges_total_vat__, __local_sale_reverse_charges_sales_gross__, __local_sale_reverse_charges_refunds_gross__, __local_sale_reverse_charges_total_gross__
        ) = TaxRecordService.get_amounts_local_sales_reverse_charge(sales, refunds)

        (
            __distance_sales_sales_net__, __distance_sales_refunds_net__,
            distance_sales_total_net,  # this is the only variable of interest
            __distance_sales_sales_vat__, __distance_sales_refunds_vat__, __distance_sales_total_vat__, __distance_sales_sales_gross__, __distance_sales_refunds_gross__, __distance_sales_total_gross__
        ) = TaxRecordService.get_amounts_distance_sales(sales, refunds)

        (
            __intra_community_sales_sales_net_case_a__, __intra_community_sales_sales_net_case_b__, __intra_community_sales_sales_net__, __intra_community_sales_refunds_net__,
            intra_community_sales_total_net  # this is the only variable of interest
        ) = TaxRecordService.get_amounts_intra_community_sales(sales, movements)

        taxable_turnover_amount = TaxRecordService.calculate_taxable_turnover_amount(local_sales_total_net, local_sale_reverse_charges_total_net, distance_sales_total_net, intra_community_sales_total_net)

        return taxable_turnover_amount






    @staticmethod
    def get_amounts_local_sales(sales: List[Transaction], refunds: List[Transaction]) -> List[float]:
         # LOCAL SALES
        local_sales_sales_net = TaxRecordService.get_invoice_net(sales, 'LOCAL_SALE')
        local_sales_refunds_net = TaxRecordService.get_invoice_net(refunds, 'LOCAL_SALE')
        local_sales_total_net = sum((local_sales_sales_net, local_sales_refunds_net))

        local_sales_sales_vat = TaxRecordService.get_invoice_vat(sales, 'LOCAL_SALE')
        local_sales_refunds_vat = TaxRecordService.get_invoice_vat(refunds, 'LOCAL_SALE')
        local_sales_total_vat = sum((local_sales_sales_vat, local_sales_refunds_vat))

        local_sales_sales_gross = TaxRecordService.get_invoice_gross(sales, 'LOCAL_SALE')
        local_sales_refunds_gross = TaxRecordService.get_invoice_gross(refunds, 'LOCAL_SALE')
        local_sales_total_gross = sum((local_sales_sales_gross, local_sales_refunds_gross))

        return (
            local_sales_sales_net,
            local_sales_refunds_net,
            local_sales_total_net,
            local_sales_sales_vat,
            local_sales_refunds_vat,
            local_sales_total_vat,
            local_sales_sales_gross,
            local_sales_refunds_gross,
            local_sales_total_gross
        )


    @staticmethod
    def get_amounts_local_sales_reverse_charge(sales: List[Transaction], refunds: List[Transaction]) -> List[float]:
         # LOCAL SALES REVERSE CHARGE
        local_sale_reverse_charges_sales_net = TaxRecordService.get_invoice_net(sales, 'LOCAL_SALE_REVERSE_CHARGE')
        local_sale_reverse_charges_refunds_net = TaxRecordService.get_invoice_net(refunds, 'LOCAL_SALE_REVERSE_CHARGE')
        local_sale_reverse_charges_total_net = sum((local_sale_reverse_charges_sales_net, local_sale_reverse_charges_refunds_net))

        local_sale_reverse_charges_sales_vat = TaxRecordService.get_invoice_vat(sales, 'LOCAL_SALE_REVERSE_CHARGE')
        local_sale_reverse_charges_refunds_vat = TaxRecordService.get_invoice_vat(refunds, 'LOCAL_SALE_REVERSE_CHARGE')
        local_sale_reverse_charges_total_vat = sum((local_sale_reverse_charges_sales_vat, local_sale_reverse_charges_refunds_vat))

        local_sale_reverse_charges_sales_gross = TaxRecordService.get_invoice_gross(sales, 'LOCAL_SALE_REVERSE_CHARGE')
        local_sale_reverse_charges_refunds_gross = TaxRecordService.get_invoice_gross(refunds, 'LOCAL_SALE_REVERSE_CHARGE')
        local_sale_reverse_charges_total_gross = sum((local_sale_reverse_charges_sales_gross, local_sale_reverse_charges_refunds_gross))

        return (
            local_sale_reverse_charges_sales_net,
            local_sale_reverse_charges_refunds_net,
            local_sale_reverse_charges_total_net,
            local_sale_reverse_charges_sales_vat,
            local_sale_reverse_charges_refunds_vat,
            local_sale_reverse_charges_total_vat,
            local_sale_reverse_charges_sales_gross,
            local_sale_reverse_charges_refunds_gross,
            local_sale_reverse_charges_total_gross
        )


    @staticmethod
    def get_amounts_distance_sales(sales: List[Transaction], refunds: List[Transaction]) -> List[float]:
        # DISTANCE SALES
        distance_sales_sales_net = TaxRecordService.get_invoice_net(sales, 'DISTANCE_SALE')
        distance_sales_refunds_net = TaxRecordService.get_invoice_net(refunds, 'DISTANCE_SALE')
        distance_sales_total_net = sum((distance_sales_sales_net, distance_sales_refunds_net))

        distance_sales_sales_vat = TaxRecordService.get_invoice_vat(sales, 'DISTANCE_SALE')
        distance_sales_refunds_vat = TaxRecordService.get_invoice_vat(refunds, 'DISTANCE_SALE')
        distance_sales_total_vat = sum((distance_sales_sales_vat, distance_sales_refunds_vat))

        distance_sales_sales_gross = TaxRecordService.get_invoice_gross(sales, 'DISTANCE_SALE')
        distance_sales_refunds_gross = TaxRecordService.get_invoice_gross(refunds, 'DISTANCE_SALE')
        distance_sales_total_gross = sum((distance_sales_sales_gross, distance_sales_refunds_gross))

        return (
            distance_sales_sales_net,
            distance_sales_refunds_net,
            distance_sales_total_net,
            distance_sales_sales_vat,
            distance_sales_refunds_vat,
            distance_sales_total_vat,
            distance_sales_sales_gross,
            distance_sales_refunds_gross,
            distance_sales_total_gross
        )

    @staticmethod
    def get_amounts_non_taxable_distance_sales(sales: List[Transaction], refunds: List[Transaction]) -> List[float]:
        # NON TAXABLE DISTANCE SALES
        non_taxable_distance_sales_sales_net = TaxRecordService.get_invoice_net(sales, 'NON_TAXABLE_DISTANCE_SALE')
        non_taxable_distance_sales_refunds_net = TaxRecordService.get_invoice_net(refunds, 'NON_TAXABLE_DISTANCE_SALE')
        non_taxable_distance_sales_total_net = sum((non_taxable_distance_sales_sales_net, non_taxable_distance_sales_refunds_net))

        non_taxable_distance_sales_sales_vat = TaxRecordService.get_invoice_vat(sales, 'NON_TAXABLE_DISTANCE_SALE')
        non_taxable_distance_sales_refunds_vat = TaxRecordService.get_invoice_vat(refunds, 'NON_TAXABLE_DISTANCE_SALE')
        non_taxable_distance_sales_total_vat = sum((non_taxable_distance_sales_sales_vat, non_taxable_distance_sales_refunds_vat))

        non_taxable_distance_sales_sales_gross = TaxRecordService.get_invoice_gross(sales, 'NON_TAXABLE_DISTANCE_SALE')
        non_taxable_distance_sales_refunds_gross = TaxRecordService.get_invoice_gross(refunds, 'NON_TAXABLE_DISTANCE_SALE')
        non_taxable_distance_sales_total_gross = sum((non_taxable_distance_sales_sales_gross, non_taxable_distance_sales_refunds_gross))


        return (
            non_taxable_distance_sales_sales_net,
            non_taxable_distance_sales_refunds_net,
            non_taxable_distance_sales_total_net,
            non_taxable_distance_sales_sales_vat,
            non_taxable_distance_sales_refunds_vat,
            non_taxable_distance_sales_total_vat,
            non_taxable_distance_sales_sales_gross,
            non_taxable_distance_sales_refunds_gross,
            non_taxable_distance_sales_total_gross
        )


    @staticmethod
    def get_amounts_intra_community_sales(sales: List[Transaction], movements: List[Transaction]) -> List[float]:
        # INTRA COMMUNITY SALES
        intra_community_sales_sales_net_case_a = TaxRecordService.get_invoice_net(sales, 'INTRA_COMMUNITY_SALE')
        intra_community_sales_sales_net_case_b = TaxRecordService.get_invoice_net(movements, 'INTRA_COMMUNITY_SALE')

        intra_community_sales_sales_net = sum((intra_community_sales_sales_net_case_a, intra_community_sales_sales_net_case_b))
        intra_community_sales_refunds_net = 0
        intra_community_sales_total_net = sum((intra_community_sales_sales_net, intra_community_sales_refunds_net))

        return (
            intra_community_sales_sales_net_case_a,
            intra_community_sales_sales_net_case_b,
            intra_community_sales_sales_net,
            intra_community_sales_refunds_net,
            intra_community_sales_total_net
        )


    @staticmethod
    def get_amounts_exports(sales: List[Transaction], refunds: List[Transaction]) -> List[float]:
        # EXPORTS
        exports_sales_net = TaxRecordService.get_invoice_net(sales, 'EXPORT')
        exports_refunds_net = TaxRecordService.get_invoice_net(refunds, 'EXPORT')
        exports_total_net = sum((exports_sales_net, exports_refunds_net))

        return (
            exports_sales_net,
            exports_refunds_net,
            exports_total_net
        )


    @staticmethod
    def get_amounts_icas(movements: List[Transaction]) -> List[float]:
         # INTRA COMMUNITY ACQUISITIONS
        ica_acquisitions_net = TaxRecordService.get_invoice_net(movements, 'INTRA_COMMUNITY_ACQUISITION')
        ica_refunds_net = 0
        ica_total_net = sum((ica_acquisitions_net, ica_refunds_net))

        ica_acquisitions_reverse_charge_vat = TaxRecordService.get_reverse_charge_vat(movements, 'INTRA_COMMUNITY_ACQUISITION')
        ica_refunds_reverse_charge_vat = 0
        ica_total_reverse_charge_vat = sum((ica_acquisitions_reverse_charge_vat, ica_refunds_reverse_charge_vat))

        return (
            ica_acquisitions_net,
            ica_refunds_net,
            ica_total_net,
            ica_acquisitions_reverse_charge_vat,
            ica_refunds_reverse_charge_vat,
            ica_total_reverse_charge_vat
        )


    @staticmethod
    def get_amounts_local_acquisitions(acquisitions: List[Transaction]) -> List[float]:

        # LOCAL ACQUISITIONS
        local_acquisitions_acquisitions_net = TaxRecordService.get_invoice_net(acquisitions, 'LOCAL_ACQUISITION')
        local_acquisitions_refunds_net = 0
        local_acquisitions_total_net = sum((local_acquisitions_acquisitions_net, local_acquisitions_refunds_net))

        local_acquisitions_acquisitions_vat = TaxRecordService.get_invoice_vat(acquisitions, 'LOCAL_ACQUISITION')
        local_acquisitions_refunds_vat = 0
        local_acquisitions_total_vat = sum((local_acquisitions_acquisitions_vat, local_acquisitions_refunds_vat))

        local_acquisitions_acquisitions_gross = TaxRecordService.get_invoice_gross(acquisitions, 'LOCAL_ACQUISITION')
        local_acquisitions_refunds_gross = 0
        local_acquisitions_total_gross = sum((local_acquisitions_acquisitions_gross, local_acquisitions_refunds_gross))

        return (
            local_acquisitions_acquisitions_net,
            local_acquisitions_refunds_net,
            local_acquisitions_total_net,
            local_acquisitions_acquisitions_vat,
            local_acquisitions_refunds_vat,
            local_acquisitions_total_vat,
            local_acquisitions_acquisitions_gross,
            local_acquisitions_refunds_gross,
            local_acquisitions_total_gross
        )


    @staticmethod
    def get_payable_vat_amount(local_sales_total_vat: float, distance_sales_total_vat: float, local_acquisitions_total_vat: float) -> List[float]:
        return (
            local_sales_total_vat
            + distance_sales_total_vat
            - local_acquisitions_total_vat
        )








    @staticmethod
    def calculate_taxable_turnover_amount(local_sales_total_net: float, local_sale_reverse_charges_total_net: float, distance_sales_total_net: float, intra_community_sales_total_net: float) -> float:
        return sum((local_sales_total_net, local_sale_reverse_charges_total_net, distance_sales_total_net, intra_community_sales_total_net))

    @staticmethod
    def create_by_seller_firm_public_id(seller_firm_public_id: str, user_id: int, tax_record_data_raw: TaxRecordInterface):

        object_type = 'tax_record'

        try:
            seller_firm, start_date, end_date, tax_jurisdiction, vatin, transactions = TaxRecordService.retrieve_input_vars(object_type, seller_firm_public_id, tax_record_data_raw)
        except Exception as e:
            if e.code == 422:
                SocketService.emit_status_error_unidentifiable_object(object_type, e.description, 0)
            elif e.code == 404:
                SocketService.emit_status_error(object_type, e.description)
            elif e.code == 417:
                SocketService.emit_status_info(object_type, e.description)
            return False


        tax_record = TaxRecordService.get_by_seller_firm_tax_jurisdiction_validity(seller_firm.id, tax_jurisdiction.code, start_date, end_date)
        if isinstance(tax_record, TaxRecord):
            message = 'Success'
            SocketService.emit_status_info(object_type, message)
            return tax_record

        sales, refunds, acquisitions, movements = TransactionExportService.separate_transactions_by_type(transactions)


        # LOCAL SALES
        (
            local_sales_sales_net,
            local_sales_refunds_net,
            local_sales_total_net,
            local_sales_sales_vat,
            local_sales_refunds_vat,
            local_sales_total_vat,
            local_sales_sales_gross,
            local_sales_refunds_gross,
            local_sales_total_gross
        ) = TaxRecordService.get_amounts_local_sales(sales, refunds)


        # LOCAL SALES REVERSE CHARGE
        (
            local_sale_reverse_charges_sales_net,
            local_sale_reverse_charges_refunds_net,
            local_sale_reverse_charges_total_net,
            local_sale_reverse_charges_sales_vat,
            local_sale_reverse_charges_refunds_vat,
            local_sale_reverse_charges_total_vat,
            local_sale_reverse_charges_sales_gross,
            local_sale_reverse_charges_refunds_gross,
            local_sale_reverse_charges_total_gross
        ) = TaxRecordService.get_amounts_local_sales_reverse_charge(sales, refunds)


        # DISTANCE SALES
        (
            distance_sales_sales_net,
            distance_sales_refunds_net,
            distance_sales_total_net,
            distance_sales_sales_vat,
            distance_sales_refunds_vat,
            distance_sales_total_vat,
            distance_sales_sales_gross,
            distance_sales_refunds_gross,
            distance_sales_total_gross
        ) = TaxRecordService.get_amounts_distance_sales(sales, refunds)


        # NON TAXABLE DISTANCE SALES
        (
            non_taxable_distance_sales_sales_net,
            non_taxable_distance_sales_refunds_net,
            non_taxable_distance_sales_total_net,
            non_taxable_distance_sales_sales_vat,
            non_taxable_distance_sales_refunds_vat,
            non_taxable_distance_sales_total_vat,
            non_taxable_distance_sales_sales_gross,
            non_taxable_distance_sales_refunds_gross,
            non_taxable_distance_sales_total_gross
        ) = TaxRecordService.get_amounts_non_taxable_distance_sales(sales, refunds)


        # INTRA COMMUNITY SALES
        (
            intra_community_sales_sales_net_case_a,
            intra_community_sales_sales_net_case_b,
            intra_community_sales_sales_net,
            intra_community_sales_refunds_net,
            intra_community_sales_total_net
        ) = TaxRecordService.get_amounts_intra_community_sales(sales, movements)


        # EXPORTS
        (
            exports_sales_net,
            exports_refunds_net,
            exports_total_net
        ) = TaxRecordService.get_amounts_exports(sales, refunds)


        # INTRA COMMUNITY ACQUISITIONS
        (
            ica_acquisitions_net,
            ica_refunds_net,
            ica_total_net,
            ica_acquisitions_reverse_charge_vat,
            ica_refunds_reverse_charge_vat,
            ica_total_reverse_charge_vat
        ) = TaxRecordService.get_amounts_icas(movements)


        # LOCAL ACQUISITIONS
        (
            local_acquisitions_acquisitions_net,
            local_acquisitions_refunds_net,
            local_acquisitions_total_net,
            local_acquisitions_acquisitions_vat,
            local_acquisitions_refunds_vat,
            local_acquisitions_total_vat,
            local_acquisitions_acquisitions_gross,
            local_acquisitions_refunds_gross,
            local_acquisitions_total_gross
        ) = TaxRecordService.get_amounts_local_acquisitions(acquisitions)


        # SUMMARY
        taxable_turnover_amount = TaxRecordService.calculate_taxable_turnover_amount(local_sales_total_net, local_sale_reverse_charges_total_net, distance_sales_total_net, intra_community_sales_total_net)
        payable_vat_amount = TaxRecordService.get_payable_vat_amount(local_sales_total_vat, distance_sales_total_vat, local_acquisitions_total_vat)

        tax_record_data = {
            'created_by': user_id,
            'seller_firm_id': seller_firm.id,

            'start_date': start_date,
            'end_date': end_date,
            'tax_jurisdiction_code': tax_jurisdiction.code,
            'currency_code': tax_jurisdiction.currency_code,

            'vatin_id': vatin.id,

            'local_sales_sales_net': local_sales_sales_net,
            'local_sales_refunds_net': local_sales_refunds_net,
            'local_sales_total_net': local_sales_total_net,
            'local_sales_sales_vat': local_sales_sales_vat,
            'local_sales_refunds_vat': local_sales_refunds_vat,
            'local_sales_total_vat': local_sales_total_vat,
            'local_sales_sales_gross': local_sales_sales_gross,
            'local_sales_refunds_gross': local_sales_refunds_gross,
            'local_sales_total_gross': local_sales_total_gross,

            'local_sale_reverse_charges_sales_net': local_sale_reverse_charges_sales_net,
            'local_sale_reverse_charges_refunds_net': local_sale_reverse_charges_refunds_net,
            'local_sale_reverse_charges_total_net': local_sale_reverse_charges_total_net,
            'local_sale_reverse_charges_sales_vat': local_sale_reverse_charges_sales_vat,
            'local_sale_reverse_charges_refunds_vat': local_sale_reverse_charges_refunds_vat,
            'local_sale_reverse_charges_total_vat': local_sale_reverse_charges_total_vat,
            'local_sale_reverse_charges_sales_gross': local_sale_reverse_charges_sales_gross,
            'local_sale_reverse_charges_refunds_gross': local_sale_reverse_charges_refunds_gross,
            'local_sale_reverse_charges_total_gross': local_sale_reverse_charges_total_gross,

            'distance_sales_sales_net': distance_sales_sales_net,
            'distance_sales_refunds_net': distance_sales_refunds_net,
            'distance_sales_total_net': distance_sales_total_net,
            'distance_sales_sales_vat': distance_sales_sales_vat,
            'distance_sales_refunds_vat': distance_sales_refunds_vat,
            'distance_sales_total_vat': distance_sales_total_vat,
            'distance_sales_sales_gross': distance_sales_sales_gross,
            'distance_sales_refunds_gross': distance_sales_refunds_gross,
            'distance_sales_total_gross': distance_sales_total_gross,

            'non_taxable_distance_sales_sales_net': non_taxable_distance_sales_sales_net,
            'non_taxable_distance_sales_refunds_net': non_taxable_distance_sales_refunds_net,
            'non_taxable_distance_sales_total_net': non_taxable_distance_sales_total_net,
            'non_taxable_distance_sales_sales_vat': non_taxable_distance_sales_sales_vat,
            'non_taxable_distance_sales_refunds_vat': non_taxable_distance_sales_refunds_vat,
            'non_taxable_distance_sales_total_vat': non_taxable_distance_sales_total_vat,
            'non_taxable_distance_sales_sales_gross': non_taxable_distance_sales_sales_gross,
            'non_taxable_distance_sales_refunds_gross': non_taxable_distance_sales_refunds_gross,
            'non_taxable_distance_sales_total_gross': non_taxable_distance_sales_total_gross,

            'intra_community_sales_sales_net': intra_community_sales_sales_net,
            'intra_community_sales_refunds_net': intra_community_sales_refunds_net,
            'intra_community_sales_total_net': intra_community_sales_total_net,

            'exports_sales_net': exports_sales_net,
            'exports_refunds_net': exports_refunds_net,
            'exports_total_net': exports_total_net,

            'ica_acquisitions_net': ica_acquisitions_net,
            'ica_refunds_net': ica_refunds_net,
            'ica_total_net': ica_total_net,
            'ica_acquisitions_reverse_charge_vat': ica_acquisitions_reverse_charge_vat,
            'ica_refunds_reverse_charge_vat': ica_refunds_reverse_charge_vat,
            'ica_total_reverse_charge_vat': ica_total_reverse_charge_vat,

            'local_acquisitions_acquisitions_net': local_acquisitions_acquisitions_net,
            'local_acquisitions_refunds_net': local_acquisitions_refunds_net,
            'local_acquisitions_total_net': local_acquisitions_total_net,
            'local_acquisitions_acquisitions_vat': local_acquisitions_acquisitions_vat,
            'local_acquisitions_refunds_vat': local_acquisitions_refunds_vat,
            'local_acquisitions_total_vat': local_acquisitions_total_vat,
            'local_acquisitions_acquisitions_gross': local_acquisitions_acquisitions_gross,
            'local_acquisitions_refunds_gross': local_acquisitions_refunds_gross,
            'local_acquisitions_total_gross': local_acquisitions_total_gross,

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

        # send status update via socket
        SocketService.emit_status_success(1, 1, 'successbox', object_type)

        # push new tax record
        tax_record_json = TaxRecordSubSchema.get_tax_record_sub(tax_record)
        SocketService.emit_new_object(tax_record_json, object_type)

        return tax_record



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
    def get_reverse_charge_vat(transactions: List[Transaction], tax_treatment_code: str):
        return sum([transaction.invoice_amount_reverse_charge_vat for transaction in transactions if transaction.tax_treatment_code == tax_treatment_code]) if not len(transactions) == 0 else 0







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

            local_sales_sales_net = tax_record_data.get('local_sales_sales_net'),
            local_sales_refunds_net = tax_record_data.get('local_sales_refunds_net'),
            local_sales_total_net = tax_record_data.get('local_sales_total_net'),
            local_sales_sales_vat = tax_record_data.get('local_sales_sales_vat'),
            local_sales_refunds_vat = tax_record_data.get('local_sales_refunds_vat'),
            local_sales_total_vat = tax_record_data.get('local_sales_total_vat'),
            local_sales_sales_gross = tax_record_data.get('local_sales_sales_gross'),
            local_sales_refunds_gross = tax_record_data.get('local_sales_refunds_gross'),
            local_sales_total_gross = tax_record_data.get('local_sales_total_gross'),

            local_sale_reverse_charges_sales_net = tax_record_data.get('local_sale_reverse_charges_sales_net'),
            local_sale_reverse_charges_refunds_net = tax_record_data.get('local_sale_reverse_charges_refunds_net'),
            local_sale_reverse_charges_total_net = tax_record_data.get('local_sale_reverse_charges_total_net'),
            local_sale_reverse_charges_sales_vat = tax_record_data.get('local_sale_reverse_charges_sales_vat'),
            local_sale_reverse_charges_refunds_vat = tax_record_data.get('local_sale_reverse_charges_refunds_vat'),
            local_sale_reverse_charges_total_vat = tax_record_data.get('local_sale_reverse_charges_total_vat'),
            local_sale_reverse_charges_sales_gross = tax_record_data.get('local_sale_reverse_charges_sales_gross'),
            local_sale_reverse_charges_refunds_gross = tax_record_data.get('local_sale_reverse_charges_refunds_gross'),
            local_sale_reverse_charges_total_gross = tax_record_data.get('local_sale_reverse_charges_total_gross'),

            distance_sales_sales_net = tax_record_data.get('distance_sales_sales_net'),
            distance_sales_refunds_net = tax_record_data.get('distance_sales_refunds_net'),
            distance_sales_total_net = tax_record_data.get('distance_sales_total_net'),
            distance_sales_sales_vat = tax_record_data.get('distance_sales_sales_vat'),
            distance_sales_refunds_vat = tax_record_data.get('distance_sales_refunds_vat'),
            distance_sales_total_vat = tax_record_data.get('distance_sales_total_vat'),
            distance_sales_sales_gross = tax_record_data.get('distance_sales_sales_gross'),
            distance_sales_refunds_gross = tax_record_data.get('distance_sales_refunds_gross'),
            distance_sales_total_gross = tax_record_data.get('distance_sales_total_gross'),

            non_taxable_distance_sales_sales_net = tax_record_data.get('non_taxable_distance_sales_sales_net'),
            non_taxable_distance_sales_refunds_net = tax_record_data.get('non_taxable_distance_sales_refunds_net'),
            non_taxable_distance_sales_total_net = tax_record_data.get('non_taxable_distance_sales_total_net'),
            non_taxable_distance_sales_sales_vat = tax_record_data.get('non_taxable_distance_sales_sales_vat'),
            non_taxable_distance_sales_refunds_vat = tax_record_data.get('non_taxable_distance_sales_refunds_vat'),
            non_taxable_distance_sales_total_vat = tax_record_data.get('non_taxable_distance_sales_total_vat'),
            non_taxable_distance_sales_sales_gross = tax_record_data.get('non_taxable_distance_sales_sales_gross'),
            non_taxable_distance_sales_refunds_gross = tax_record_data.get('non_taxable_distance_sales_refunds_gross'),
            non_taxable_distance_sales_total_gross = tax_record_data.get('non_taxable_distance_sales_total_gross'),

            intra_community_sales_sales_net = tax_record_data.get('intra_community_sales_sales_net'),
            intra_community_sales_refunds_net = tax_record_data.get('intra_community_sales_refunds_net'),
            intra_community_sales_total_net = tax_record_data.get('intra_community_sales_total_net'),

            exports_sales_net = tax_record_data.get('exports_sales_net'),
            exports_refunds_net = tax_record_data.get('exports_refunds_net'),
            exports_total_net = tax_record_data.get('exports_total_net'),

            ica_acquisitions_net = tax_record_data.get('ica_acquisitions_net'),
            ica_refunds_net = tax_record_data.get('ica_refunds_net'),
            ica_total_net = tax_record_data.get('ica_total_net'),
            ica_acquisitions_reverse_charge_vat = tax_record_data.get('ica_acquisitions_reverse_charge_vat'),
            ica_refunds_reverse_charge_vat = tax_record_data.get('ica_refunds_reverse_charge_vat'),
            ica_total_reverse_charge_vat = tax_record_data.get('ica_total_reverse_charge_vat'),

            local_acquisitions_acquisitions_net = tax_record_data.get('local_acquisitions_acquisitions_net'),
            local_acquisitions_refunds_net = tax_record_data.get('local_acquisitions_refunds_net'),
            local_acquisitions_total_net = tax_record_data.get('local_acquisitions_total_net'),
            local_acquisitions_acquisitions_vat = tax_record_data.get('local_acquisitions_acquisitions_vat'),
            local_acquisitions_refunds_vat = tax_record_data.get('local_acquisitions_refunds_vat'),
            local_acquisitions_total_vat = tax_record_data.get('local_acquisitions_total_vat'),
            local_acquisitions_acquisitions_gross = tax_record_data.get('local_acquisitions_acquisitions_gross'),
            local_acquisitions_refunds_gross = tax_record_data.get('local_acquisitions_refunds_gross'),
            local_acquisitions_total_gross = tax_record_data.get('local_acquisitions_total_gross'),

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




class TaxRecordExportService:

    @staticmethod
    def generate_tax_record_export(tax_record: TaxRecord):

        (
            local_sales,
            local_sales_reverse_charge,
            distance_sales,
            non_taxable_distance_sales,
            intra_community_sales,
            exports,
            local_acquisitions,
            intra_community_acquisitions
        ) = TransactionExportService.separate_transactions_by_tax_treatment(tax_record.transactions)

        seller_firm_name = tax_record.seller_firm.name


        df.to_csv(os.path.join(baseDir, tax_record.filename), mode="a", header=False)

        #bad code
        df = pd.read_csv(os.path.join(baseDir, tax_record.filename))
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.drop_duplicates()
        df=df.reset_index(drop=True)
        df.to_csv(os.path.join(baseDir, tax_record.filename), mode="w", header=True)










    # @staticmethod
    # def get_df_list(tax_record_dict: TaxRecordDictInterface) -> List[Union[pd.DataFrame, str]]:
    #     tab_names = ['LOCAL_SALES', 'LOCAL_SALES_REVERSE_CHARGE', 'DISTANCE_SALES', 'NON_TAXABLE_DISTANCE_SALES', 'INTRA_COMMUNITY_SALES', 'EXPORTS', 'LOCAL_ACQUISITIONS', 'INTRA_COMMUNITY_ACQUISITIONS']
    #     #'SUMMARY',
    #     df_local_sales = pd.Dataframe(tax_record_dict.get('LOCAL_SALES'))
    #     df_local_sales_reverse_charge = pd.Dataframe(tax_record_dict.get('LOCAL_SALES_REVERSE_CHARGE'))
    #     df_distance_sales = pd.Dataframe(tax_record_dict.get('DISTANCE_SALES'))
    #     df_non_taxable_distance_sales = pd.Dataframe(tax_record_dict.get('NON_TAXABLE_DISTANCE_SALES'))
    #     df_intra_community_sales = pd.Dataframe(tax_record_dict.get('INTRA_COMMUNITY_SALES'))
    #     df_exports = pd.Dataframe(tax_record_dict.get('EXPORTS'))
    #     df_domestic_acquisitions = pd.Dataframe(tax_record_dict.get('LOCAL_ACQUISITIONS'))
    #     df_ica = pd.Dataframe(tax_record_dict.get('INTRA_COMMUNITY_ACQUISITIONS'))
    #     #df_summary = TaxRecordService.calculate_front_page(df_local_sales, df_local_sales_reverse_charge, df_distance_sales, df_non_taxable_distance_sales, df_intra_community_sales, df_exports, df_domestic_acquisitions, df_ica)

    #     df_list = [df_local_sales, df_local_sales_reverse_charge, df_distance_sales, df_non_taxable_distance_sales, df_intra_community_sales, df_exports, df_domestic_acquisitions, df_ica]
    #     #df_summary,

    #     # !!! evtl. dies für summary :
    #     # ####

    #     #             https: // stackoverflow.com/questions/18423298/easy-way-to-fill-in-an-excel-file-with-python



    #     # ####


    #     return tab_names, df_list






    #     # @staticmethod
    #     # !!! def calculate_front_page(df_local_sales: pd.DataFrame, df_local_sales_reverse_charge: pd.DataFrame, df_distance_sales: pd.DataFrame, df_non_taxable_distance_sales: pd.DataFrame, df_intra_community_sales: pd.DataFrame, df_exports: pd.DataFrame, df_domestic_acquisitions: pd.DataFrame, df_ica: pd.DataFrame) -> pd.DataFrame:

    #     #     ### something happens here


    #     #     return df_summary





    #     @staticmethod
    #     def write_dfs_to_xlsx(df_list, tab_names, file_path):
    #         writer=pd.ExcelWriter(path=file_path, engine='xlsxwriter')
    #         for dataframe, sheet in zip(df_list, tab_names):
    #             dataframe.to_excel(writer, sheet_name=sheet, startrow=0, startcol=0)
    #             writer.save()






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

    #             'CUSTOMER_FIRM_VAT_NUMBER_COUNTRY': customer_vatin.country_code if isinstance(customer_vatin, VATIN) else None,
    #             'CUSTOMER_FIRM_VAT_NUMBER': customer_vatin.number if isinstance(customer_vatin, VATIN) else None,
    #             'CUSTOMER_FIRM_VAT_VALID': customer_vatin.valid if isinstance(customer_vatin, VATIN) else None,
    #             'CUSTOMER_FIRM_VAT_CHECKED_DATE': customer_vatin.created_on if isinstance(customer_vatin, VATIN) else None,

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
