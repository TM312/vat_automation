from flask_restx import Model, fields

from ..transaction import transaction_sub_dto

tax_record_sub_dto = Model('tax_record_sub', {
    'public_id': fields.String(readonly=True),
    'tax_jurisdiction_code': fields.String(readonly=True),
    'start_date': fields.Date(readonly=True),
    'end_date': fields.Date(readonly=True),
    'seller_firm_public_id': fields.String(attribute=lambda x: x.seller_firm.public_id, readonly=True),
})

tax_record_dto = tax_record_sub_dto.clone('tax_record', {
    'created_on': fields.DateTime(readonly=True),
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'vatin': fields.String(attribute=lambda x: '{}-{}'.format(x.vatin.country_code, x.vatin.number)),
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),

    'taxable_turnover_amount': fields.Float(readonly=True),
    'payable_vat_amount': fields.Float(readonly=True),


    'total_local_sale': fields.Float(readonly=True),
    'total_local_sale_reverse_charge': fields.Float(readonly=True),
    'total_distance_sale': fields.Float(readonly=True),
    'total_non_taxable_distance_sale': fields.Float(readonly=True),
    'total_intra_community_sale': fields.Float(readonly=True),
    'total_export': fields.Float(readonly=True),
    'total_local_acquisition': fields.Float(readonly=True),
    'total_intra_community_acquisition': fields.Float(readonly=True),
    'total_import': fields.Float(readonly=True),
    'transactions':fields.List(fields.Nested(transaction_sub_dto))
})

tax_record_dto_admin = tax_record_dto.clone('tax_record_admin', {
    'id': fields.Integer(readonly=True),
    'seller_firm_id': fields.String(readonly=True)

})
