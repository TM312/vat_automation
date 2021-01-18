from flask_restx import Model, fields
from ..schema_parent import business_dto, business_sub_dto, business_admin_dto

import app.namespaces.distance_sale as distance_sale
import app.namespaces.account as account
import app.namespaces.item as item
import app.namespaces.tax.vatin as vatin
import app.namespaces.tax_record as tax_record
#import app.namespaces.transaction as transaction



# from app.namespaces.transaction_input import transaction_input_sub_dto
accounting_firm_sub_dto = business_sub_dto.clone('accounting_firm_sub', {
})

tax_auditor_sub_dto = Model('tax_auditor_sub', {
    'public_id': fields.String(readonly=True),
    'registered_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'last_seen': fields.DateTime(readonly=True),
    'role': fields.String(readonly=True),
    'name': fields.String,
    'initials': fields.String,
})


seller_firm_sub_dto = business_sub_dto.clone('seller_firm_sub', {
    'claimed': fields.Boolean(readonly=True),
    'establishment_country_code': fields.String,
    # 'establishment_country': fields.String(attribute=lambda x: x.establishment_country.name if x.establishment_country else None),
    'transaction_ready': fields.Boolean(readonly=True),
})
seller_firm_dto = seller_firm_sub_dto.clone('seller_firm', {
    'created_by': fields.String(attribute=lambda x: x.creator.name if isinstance(x.created_by, int) else None),
    'created_on': fields.Date(readonly=True),
    'tax_auditors': fields.List(fields.Nested(tax_auditor_sub_dto)),
    'accounting_firms': fields.List(fields.Nested(accounting_firm_sub_dto)),
    'items': fields.List(fields.Nested(item.item_sub_dto)),
    'distance_sales': fields.List(fields.Nested(distance_sale.distance_sale_sub_dto)),
    'accounts': fields.List(fields.Nested(account.account_sub_dto)),
    'vat_numbers': fields.List(fields.Nested(vatin.vatin_sub_dto)),
    # 'transactions': fields.List(fields.Nested(transaction_sub_dto)),
    # 'transaction_inputs': fields.List(fields.Nested(transaction_input_sub_dto)),
    'tax_records': fields.List(fields.Nested(tax_record.tax_record_sub_dto)),
})
seller_firm_admin_dto = seller_firm_dto.clone('seller_firm_admin', {
    'id': fields.Integer(readonly=True)
})
