from flask_restx import Model, fields

from app.namespaces.transaction import transaction_dto


transaction_input_sub_dto = Model('transaction_input_sub', {
    'public_id': fields.String(readonly=True),
    'processed': fields.Boolean,
    'channel_code': fields.String,
    'marketplace': fields.String,
    'given_id': fields.String,
    'transaction_type_public_code': fields.String,
    'complete_date': fields.Date,
    'item_sku': fields.String,
    'item_quantity': fields.Integer,
    'sale_total_value_gross': fields.Float,
    'currency_code': fields.String,
    'departure_country_code': fields.String,
    'arrival_country_code': fields.String,
})


transaction_input_dto = transaction_input_sub_dto.clone('transaction_input', {
    'activity_id': fields.String,
    'created_on': fields.DateTime,
    'created_by': fields.String(attribute=lambda x: x.uploader.name),
    'original_filename': fields.String,
    'bundle_public_id': fields.String(attribute=lambda x: x.bundle.public_id, readonly=True),
    'processed_on': fields.DateTime,
    'seller_firm_public_id': fields.String(attribute=lambda x: x.seller_firm.public_id, readonly=True),


    'transactions': fields.List(fields.Nested(transaction_dto)),
    'public_activity_period': fields.String,
    'account_given_id': fields.String,

    'shipment_date': fields.Date,
    'arrival_date': fields.Date,

    'item_name': fields.String,
    'item_manufacture_country': fields.String,
    'item_weight_kg': fields.Float,
    'item_weight_kg_total': fields.Float,
    'item_price_discount_gross': fields.Float,
    'item_price_gross': fields.Float,
    'item_price_total_gross': fields.Float,
    'shipment_price_discount_gross': fields.Float,
    'shipment_price_gross': fields.Float,
    'shipment_price_total_gross': fields.Float,
    'gift_wrap_price_discount_gross': fields.Float,
    'gift_wrap_price_gross': fields.Float,
    'gift_wrap_price_total_gross': fields.Float,
    'departure_postal_code': fields.String,
    'departure_city': fields.String,
    'arrival_postal_code': fields.String,
    'arrival_city': fields.String,
    'arrival_address': fields.String,
    'shipment_mode': fields.String,
    'shipment_conditions': fields.String,
    'invoice_number': fields.String,
    'invoice_url': fields.String,
    'customer_name': fields.String,
    'customer_vat_number': fields.String,
    'customer_vat_number_country_code': fields.String,
    'supplier_vat_number': fields.String,
    'supplier_name': fields.String,
    'tax_calculation_date': fields.Date,
    'unit_cost_price_net': fields.Float,
    'item_price_discount_net': fields.Float,
    'item_price_discount_vat': fields.Float,
    'item_price_net': fields.Float,
    'item_price_vat': fields.Float,
    'item_price_total_net': fields.Float,
    'item_price_total_vat': fields.Float,
    'item_price_vat': fields.Float,
    'item_price_vat_rate': fields.Float,
    'shipment_price_discount_net': fields.Float,
    'shipment_price_discount_vat': fields.Float,
    'shipment_price_net': fields.Float,
    'shipment_price_vat': fields.Float,
    'shipment_price_total_net': fields.Float,
    'shipment_price_total_vat': fields.Float,
    'shipment_price_vat': fields.Float,
    'shipment_price_vat_rate': fields.Float,
    'sale_total_value_net': fields.Float,
    'sale_total_value_vat': fields.Float,
    'gift_wrap_price_discount_net': fields.Float,
    'gift_wrap_price_discount_vat': fields.Float,
    'gift_wrap_price_net': fields.Float,
    'gift_wrap_price_vat': fields.Float,
    'gift_wrap_price_total_net': fields.Float,
    'gift_wrap_price_total_vat': fields.Float,
    'gift_wrap_price_tax_rate': fields.Float,
    'item_tax_code_code': fields.String,
    'departure_seller_vat_country_code': fields.String,
    'departure_seller_vat_number': fields.String,
    'arrival_seller_vat_country_code': fields.String,
    'arrival_seller_vat_number': fields.String,
    'seller_vat_country_code': fields.String,
    'seller_vat_number': fields.String,
    'tax_calculation_imputation_country': fields.String,
    'tax_jurisdiction': fields.String,
    'tax_jurisdiction_level': fields.String,
    'invoice_amount_vat': fields.Float,
    'invoice_currency_code': fields.String,
    'invoice_exchange_rate': fields.Float,
    'invoice_exchange_rate_date': fields.Date,
    'export': fields.Boolean
})


transaction_input_admin_dto = transaction_input_dto.clone('transaction_input_admin', {
    'id': fields.Integer(readonly=True),
    'bundle_id': fields.Integer
})



class TransactionInputSubSchema:

    @staticmethod
    def get_transaction_input_sub(transaction_input):
        transaction_input_as_dict = {
            'public_id': str(transaction_input.public_id),
            'processed': transaction_input.processed,
            'channel_code': transaction_input.channel_code,
            'marketplace': transaction_input.marketplace,
            'given_id': transaction_input.given_id,
            'transaction_type_public_code': transaction_input.transaction_type_public_code,
            'complete_date': str(transaction_input.complete_date),
            'item_sku': transaction_input.item_sku,
            'item_quantity': transaction_input.item_quantity,
            'sale_total_value_gross': transaction_input.sale_total_value_gross,
            'currency_code': transaction_input.currency_code,
            'departure_country_code': transaction_input.departure_country_code,
            'arrival_country_code': transaction_input.arrival_country_code,
            # 'seller_firm_public_id': str(transaction_input.seller_firm.public_id)
        }
        return transaction_input_as_dict
