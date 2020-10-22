from flask_restx import Model, fields

from app.namespaces.transaction import transaction_sub_dto

tax_record_sub_dto = Model('tax_record_sub', {
    'public_id': fields.String(readonly=True),
    'tax_jurisdiction_code': fields.String(readonly=True),
    'start_date': fields.Date(readonly=True),
    'end_date': fields.Date(readonly=True),
    'taxable_turnover_amount': fields.Float(readonly=True),
    'payable_vat_amount': fields.Float(readonly=True),
    'currency_code': fields.String(readonly=True)
})

tax_record_dto = tax_record_sub_dto.clone('tax_record', {
    'created_on': fields.DateTime(readonly=True),
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'vatin': fields.String(attribute=lambda x: '{}-{}'.format(x.vatin.country_code, x.vatin.number)),
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),
    'seller_firm_public_id': fields.String(attribute=lambda x: x.seller_firm.public_id, readonly=True),


    'local_sales_sales_net': fields.Float(readonly=True),
    'local_sales_refunds_net': fields.Float(readonly=True),
    'local_sales_total_net': fields.Float(readonly=True),
    'local_sales_sales_vat': fields.Float(readonly=True),
    'local_sales_refunds_vat': fields.Float(readonly=True),
    'local_sales_total_vat': fields.Float(readonly=True),
    'local_sales_sales_gross': fields.Float(readonly=True),
    'local_sales_refunds_gross': fields.Float(readonly=True),
    'local_sales_total_gross': fields.Float(readonly=True),

    'local_sale_reverse_charges_sales_net': fields.Float(readonly=True),
    'local_sale_reverse_charges_refunds_net': fields.Float(readonly=True),
    'local_sale_reverse_charges_total_net': fields.Float(readonly=True),
    'local_sale_reverse_charges_sales_vat': fields.Float(readonly=True),
    'local_sale_reverse_charges_refunds_vat': fields.Float(readonly=True),
    'local_sale_reverse_charges_total_vat': fields.Float(readonly=True),
    'local_sale_reverse_charges_sales_gross': fields.Float(readonly=True),
    'local_sale_reverse_charges_refunds_gross': fields.Float(readonly=True),
    'local_sale_reverse_charges_total_gross': fields.Float(readonly=True),

    'distance_sales_sales_net': fields.Float(readonly=True),
    'distance_sales_refunds_net': fields.Float(readonly=True),
    'distance_sales_total_net': fields.Float(readonly=True),
    'distance_sales_sales_vat': fields.Float(readonly=True),
    'distance_sales_refunds_vat': fields.Float(readonly=True),
    'distance_sales_total_vat': fields.Float(readonly=True),
    'distance_sales_sales_gross': fields.Float(readonly=True),
    'distance_sales_refunds_gross': fields.Float(readonly=True),
    'distance_sales_total_gross': fields.Float(readonly=True),

    'non_taxable_distance_sales_sales_net': fields.Float(readonly=True),
    'non_taxable_distance_sales_refunds_net': fields.Float(readonly=True),
    'non_taxable_distance_sales_total_net': fields.Float(readonly=True),
    'non_taxable_distance_sales_sales_vat': fields.Float(readonly=True),
    'non_taxable_distance_sales_refunds_vat': fields.Float(readonly=True),
    'non_taxable_distance_sales_total_vat': fields.Float(readonly=True),
    'non_taxable_distance_sales_sales_gross': fields.Float(readonly=True),
    'non_taxable_distance_sales_refunds_gross': fields.Float(readonly=True),
    'non_taxable_distance_sales_total_gross': fields.Float(readonly=True),

    'intra_community_sales_sales_net': fields.Float(readonly=True),
    'intra_community_sales_refunds_net': fields.Float(readonly=True),
    'intra_community_sales_total_net': fields.Float(readonly=True),

    'exports_sales_net': fields.Float(readonly=True),
    'exports_refunds_net': fields.Float(readonly=True),
    'exports_total_net': fields.Float(readonly=True),

    'ica_acquisitions_net': fields.Float(readonly=True),
    'ica_refunds_net': fields.Float(readonly=True),
    'ica_total_net': fields.Float(readonly=True),
    'ica_acquisitions_reverse_charge_vat': fields.Float(readonly=True),
    'ica_refunds_reverse_charge_vat': fields.Float(readonly=True),
    'ica_total_reverse_charge_vat': fields.Float(readonly=True),

    'local_acquisitions_acquisitions_net': fields.Float(readonly=True),
    'local_acquisitions_refunds_net': fields.Float(readonly=True),
    'local_acquisitions_total_net': fields.Float(readonly=True),
    'local_acquisitions_acquisitions_vat': fields.Float(readonly=True),
    'local_acquisitions_refunds_vat': fields.Float(readonly=True),
    'local_acquisitions_total_vat': fields.Float(readonly=True),
    'local_acquisitions_acquisitions_gross': fields.Float(readonly=True),
    'local_acquisitions_refunds_gross': fields.Float(readonly=True),
    'local_acquisitions_total_gross': fields.Float(readonly=True),


    'transactions':fields.List(fields.Nested(transaction_sub_dto))
})

tax_record_dto_admin = tax_record_dto.clone('tax_record_admin', {
    'id': fields.Integer(readonly=True),
    'seller_firm_id': fields.String(readonly=True)

})


class TaxRecordSubSchema:

    @staticmethod
    def get_tax_record_sub(tax_record):
        tax_record_sub_as_dict = {
            'public_id': str(tax_record.public_id),
            'tax_jurisdiction_code': tax_record.tax_jurisdiction_code,
            'start_date': str(tax_record.start_date),
            'end_date': str(tax_record.end_date),
            'taxable_turnover_amount': tax_record.taxable_turnover_amount,
            'payable_vat_amount': tax_record.payable_vat_amount,
            'currency_code': tax_record.currency_code
        }

        return tax_record_sub_as_dict
