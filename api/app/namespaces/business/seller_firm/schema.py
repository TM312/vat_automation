from flask_restx import Model, fields
from ..schema_parent import business_dto, business_sub_dto, business_admin_dto

from ...distance_sale import distance_sale_sub_dto
from ...account import account_sub_dto
from ...item import item_sub_dto
from ...tax.vatin import vatin_sub_dto
# from ...transaction_input import transaction_input_sub_dto




seller_firm_sub_dto = business_sub_dto.clone('seller_firm_sub', {
    'claimed': fields.Boolean(readonly=True),
    'establishment_country_code': fields.String,
    'establishment_country': fields.String(attribute=lambda x: x.establishment_country.name),
    'accounting_firm_name': fields.String(attribute=lambda x: x.accounting_firm.name),
    'accounting_firm_client_id': fields.String,
    'transaction_ready': fields.Boolean(readonly=True),
    'len_items': fields.Integer(attribute=lambda x: len(x.items), readonly=True),
    'len_distance_sales': fields.Integer(attribute=lambda x: len(x.distance_sales), readonly=True),
    'len_accounts': fields.Integer(attribute=lambda x: len(x.accounts), readonly=True),
    # 'len_transaction_inputs': fields.Integer(attribute=lambda x: len(x.transaction_inputs), readonly=True),
})

seller_firm_dto = seller_firm_sub_dto.clone('seller_firm', {
    'items': fields.List(fields.Nested(item_sub_dto)),
    'distance_sales': fields.List(fields.Nested(distance_sale_sub_dto)),
    'accounts': fields.List(fields.Nested(account_sub_dto)),
    'vat_numbers': fields.List(fields.Nested(vatin_sub_dto)),
    # 'transaction_inputs': fields.List(fields.Nested(transaction_input_sub_dto)),
    # 'tax_records': fields.List(fields.Nested('app.namespaces.tax_record.tax_record_dto')),
})

seller_firm_admin_dto = seller_firm_dto.clone('seller_firm_admin', {
    'id': fields.Integer(readonly=True),
    'accounting_firm_id': fields.String,
    'len_employees': fields.Integer(attribute=lambda x: len(x.employees), readonly=True),

})
