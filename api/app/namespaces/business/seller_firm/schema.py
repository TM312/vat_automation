from flask_restx import Model, fields
from ..schema_parent import business_dto, business_sub_dto

from ...distance_sale import distance_sale_sub_dto
from ...account import account_sub_dto
from ...item import item_dto
from ...tax.vatin import vatin_sub_dto




seller_firm_dto = business_dto.inherit('seller_firm', {
    'claimed': fields.Boolean(readonly=True),
    'establishment_country_code': fields.String,
    'establishment_country': fields.String(attribute=lambda x: x.establishment_country.name),
    'accounting_firm_id': fields.String,
    'accounting_firm_name': fields.String(attribute=lambda x: x.accounting_firm.name),
    'accounting_firm_client_id': fields.String,
    'transaction_ready': fields.Boolean,
    'items': fields.List(fields.Nested(item_dto)),
    'distance_sales': fields.List(fields.Nested(distance_sale_sub_dto)),
    'accounts': fields.List(fields.Nested(account_sub_dto)),
    'vat_numbers': fields.List(fields.Nested(vatin_sub_dto)),
    # 'tax_records': fields.List(fields.Nested('app.namespaces.tax_record.tax_record_dto')),
    'len_items': fields.String(attribute=lambda x: len(x.items)),
    'len_distance_sales': fields.String(attribute=lambda x: len(x.distance_sales)),
    'len_accounts': fields.String(attribute=lambda x: len(x.accounts)),
    'len_vat_numbers': fields.String(attribute=lambda x: len(x.vat_numbers))

})


seller_firm_sub_dto = business_sub_dto.inherit('seller_firm', {
    'claimed': fields.Boolean(readonly=True),
    'establishment_country_code': fields.String,
    'establishment_country': fields.String(attribute=lambda x: x.establishment_country.name),
    'accounting_firm_id': fields.String,
    'accounting_firm_name': fields.String(attribute=lambda x: x.accounting_firm.name),
    'accounting_firm_client_id': fields.String,
    'transaction_ready': fields.Boolean,
    'len_items': fields.String(attribute=lambda x: len(x.items)),
    'len_distance_sales': fields.String(attribute=lambda x: len(x.distance_sales)),
    'len_accounts': fields.String(attribute=lambda x: len(x.accounts)),
    'len_vat_numbers': fields.String(attribute=lambda x: len(x.vat_numbers))

})
