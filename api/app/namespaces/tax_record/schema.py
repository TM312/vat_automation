from flask_restx import Model, fields

from ..transaction import transaction_sub_dto

tax_record_sub_dto = Model('tax_record_sub', {
    'public_id': fields.String(readonly=True),
    'tax_jurisdiction_code': fields.String(readonly=True),
    'start_date': fields.Date(readonly=True),
    'end_date': fields.Date(readonly=True),
    'seller_firm_public_id': fields.String(attribute=lambda x: x.seller_firm.public_id, readonly=True),
    'taxable_turnover_amount': fields.Float(readonly=True),
    'payable_vat_amount': fields.Float(readonly=True),
})

tax_record_dto = tax_record_sub_dto.clone('tax_record', {
    'created_on': fields.DateTime(readonly=True),
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'vatin': fields.String(attribute=lambda x: '{}-{}'.format(x.vatin.country_code, x.vatin.number)),
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),

    'local_sales_sales_invoice_amount_net': fields.Float(readonly=True),
    'local_sales_refunds_invoice_amount_net': fields.Float(readonly=True),
    'local_sales_total_invoice_amount_net': fields.Float(readonly=True),
    'local_sales_sales_invoice_amount_vat': fields.Float(readonly=True),
    'local_sales_refunds_invoice_amount_vat': fields.Float(readonly=True),
    'local_sales_total_invoice_amount_vat': fields.Float(readonly=True),
    'local_sales_sales_invoice_amount_gross': fields.Float(readonly=True),
    'local_sales_refunds_invoice_amount_gross': fields.Float(readonly=True),
    'local_sales_total_invoice_amount_gross': fields.Float(readonly=True),

    'local_sale_reverse_charges_sales_invoice_amount_net': fields.Float(readonly=True),
    'local_sale_reverse_charges_refunds_invoice_amount_net': fields.Float(readonly=True),
    'local_sale_reverse_charges_total_invoice_amount_net': fields.Float(readonly=True),
    'local_sale_reverse_charges_sales_invoice_amount_vat': fields.Float(readonly=True),
    'local_sale_reverse_charges_refunds_invoice_amount_vat': fields.Float(readonly=True),
    'local_sale_reverse_charges_total_invoice_amount_vat': fields.Float(readonly=True),
    'local_sale_reverse_charges_sales_invoice_amount_gross': fields.Float(readonly=True),
    'local_sale_reverse_charges_refunds_invoice_amount_gross': fields.Float(readonly=True),
    'local_sale_reverse_charges_total_invoice_amount_gross': fields.Float(readonly=True),

    'distance_sales_sales_invoice_amount_net': fields.Float(readonly=True),
    'distance_sales_refunds_invoice_amount_net': fields.Float(readonly=True),
    'distance_sales_total_invoice_amount_net': fields.Float(readonly=True),
    'distance_sales_sales_invoice_amount_vat': fields.Float(readonly=True),
    'distance_sales_refunds_invoice_amount_vat': fields.Float(readonly=True),
    'distance_sales_total_invoice_amount_vat': fields.Float(readonly=True),
    'distance_sales_sales_invoice_amount_gross': fields.Float(readonly=True),
    'distance_sales_refunds_invoice_amount_gross': fields.Float(readonly=True),
    'distance_sales_total_invoice_amount_gross': fields.Float(readonly=True),

    'non_taxable_distance_sales_sales_invoice_amount_net': fields.Float(readonly=True),
    'non_taxable_distance_sales_refunds_invoice_amount_net': fields.Float(readonly=True),
    'non_taxable_distance_sales_total_invoice_amount_net': fields.Float(readonly=True),
    'non_taxable_distance_sales_sales_invoice_amount_vat': fields.Float(readonly=True),
    'non_taxable_distance_sales_refunds_invoice_amount_vat': fields.Float(readonly=True),
    'non_taxable_distance_sales_total_invoice_amount_vat': fields.Float(readonly=True),
    'non_taxable_distance_sales_sales_invoice_amount_gross': fields.Float(readonly=True),
    'non_taxable_distance_sales_refunds_invoice_amount_gross': fields.Float(readonly=True),
    'non_taxable_distance_sales_total_invoice_amount_gross': fields.Float(readonly=True),

    'intra_community_sales_sales_invoice_amount_net': fields.Float(readonly=True),
    'intra_community_sales_refunds_invoice_amount_net': fields.Float(readonly=True),
    'intra_community_sales_total_invoice_amount_net': fields.Float(readonly=True),

    'exports_sales_invoice_amount_net': fields.Float(readonly=True),
    'exports_refunds_invoice_amount_net': fields.Float(readonly=True),
    'exports_total_invoice_amount_net': fields.Float(readonly=True),

    'intra_community_acquisitions_acquisitions_invoice_amount_net': fields.Float(readonly=True),
    'intra_community_acquisitions_refunds_invoice_amount_net': fields.Float(readonly=True),
    'intra_community_acquisitions_total_invoice_amount_net': fields.Float(readonly=True),
    'intra_community_acquisitions_acquisitions_invoice_amount_vat_reverse_charge': fields.Float(readonly=True),
    'intra_community_acquisitions_refunds_invoice_amount_vat_reverse_charge': fields.Float(readonly=True),
    'intra_community_acquisitions_total_invoice_amount_vat_reverse_charge': fields.Float(readonly=True),

    'local_acquisitions_acquisitions_invoice_amount_net': fields.Float(readonly=True),
    'local_acquisitions_refunds_invoice_amount_net': fields.Float(readonly=True),
    'local_acquisitions_total_invoice_amount_net': fields.Float(readonly=True),
    'local_acquisitions_acquisitions_invoice_amount_vat': fields.Float(readonly=True),
    'local_acquisitions_refunds_invoice_amount_vat': fields.Float(readonly=True),
    'local_acquisitions_total_invoice_amount_vat': fields.Float(readonly=True),
    'local_acquisitions_acquisitions_invoice_amount_gross': fields.Float(readonly=True),
    'local_acquisitions_refunds_invoice_amount_gross': fields.Float(readonly=True),
    'local_acquisitions_total_invoice_amount_gross': fields.Float(readonly=True),


    'transactions':fields.List(fields.Nested(transaction_sub_dto))
})

tax_record_dto_admin = tax_record_dto.clone('tax_record_admin', {
    'id': fields.Integer(readonly=True),
    'seller_firm_id': fields.String(readonly=True)

})
