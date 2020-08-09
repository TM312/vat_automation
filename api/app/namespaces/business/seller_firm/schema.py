from flask_restx import Model, fields
from ..schema_parent import business_dto, business_sub_dto, business_admin_dto

from ...distance_sale import distance_sale_sub_dto
from ...account import account_sub_dto
from ...item import item_sub_dto
from ...tax.vatin import vatin_sub_dto
# from ...transaction_input import transaction_input_sub_dto




class SellerFirmSchema:

    @staticmethod
    def get_seller_firm_dto():
        from ...user.tax_auditor import tax_auditor_sub_dto
        from ...tax_record import tax_record_sub_dto
        from ...transaction import transaction_sub_dto
        return seller_firm_sub_dto.clone('seller_firm', {
            'created_by': fields.String(attribute=lambda x: x.creator.name),
            'created_on': fields.Date(readonly=True),
            'tax_auditors': fields.List(fields.Nested(tax_auditor_sub_dto)),
            'accounting_firm_name': fields.String(attribute=lambda x: x.accounting_firm.name if x.accounting_firm else None),
            'items': fields.List(fields.Nested(item_sub_dto)),
            'distance_sales': fields.List(fields.Nested(distance_sale_sub_dto)),
            'accounts': fields.List(fields.Nested(account_sub_dto)),
            'vat_numbers': fields.List(fields.Nested(vatin_sub_dto)),
            # 'transactions': fields.List(fields.Nested(transaction_sub_dto)),
            # 'transaction_inputs': fields.List(fields.Nested(transaction_input_sub_dto)),
            'tax_records': fields.List(fields.Nested(tax_record_sub_dto)),
        })


seller_firm_sub_dto = business_sub_dto.clone('seller_firm_sub', {
    'claimed': fields.Boolean(readonly=True),
    'establishment_country_code': fields.String,
    'establishment_country': fields.String(attribute=lambda x: x.establishment_country.name if x.establishment_country else None),
    'accounting_firm_client_id': fields.String,
    'transaction_ready': fields.Boolean(readonly=True),
    'accounting_firm_client_id': fields.String,
})


seller_firm_dto = SellerFirmSchema.get_seller_firm_dto()

seller_firm_admin_dto = seller_firm_dto.clone('seller_firm_admin', {
    'id': fields.Integer(readonly=True),
    'accounting_firm_id': fields.String,
    'len_employees': fields.Integer,

})
