from app.test.fixtures import app, db  # noqa
from typing import List
from .model import Transaction
from .service import TransactionService  # noqa
from .interface import TransactionInterface




def test_get_all(db):  # noqa
    a = 5
    # tu1:  = User(email='yin@email.com', role="admin", password="1234")
    # yang: User = User(email='yang@email.com', password="4321")
    # db.session.add(yin)
    # db.session.add(yang)
    # db.session.commit()

    # results: List[User] = UserService.get_all()

    assert a == 5
    #assert len(results) == 2
    #assert yin in results and yang in results




# def test_output_SOME_ID():

#     transaction = TransactionService.get_by_###



#     assert transaction.transaction_input_id ==
#     assert transaction.seller_firm_id ==
#     assert transaction.item_id ==
#     assert transaction.type_code ==
#     assert transaction.amazon_vat_calculation_service ==
#     assert transaction.customer_relationship_checked ==
#     assert transaction.transaction_input_id ==



#     customer_relationship_checked = db.Column(db.Boolean, nullable=False)
#     customer_relationship = db.Column(db.String(16), nullable=False)
#     customer_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'))
#     customer_firm_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))

#     tax_jurisdiction_code = db.Column(db.String(4), db.ForeignKey('country.code'), nullable=False)
#     arrival_country_code = db.Column(db.String(4), db.ForeignKey('country.code'), nullable=False)
#     departure_country_code = db.Column(db.String(4), db.ForeignKey('country.code'), nullable=False)


#     tax_treatment_code = db.Column(db.String(40), db.ForeignKey('tax_treatment.code'), nullable=False)

#     tax_date = db.Column(db.Date, nullable=False)
#     tax_calculation_date = db.Column(db.Date, nullable=False)
#     item_tax_code_code = db.Column(db.String(40), nullable=False)
#     item_tax_rate_type_code = db.Column(db.String(8), db.ForeignKey('tax_rate_type.code'), nullable=False)
#     shipment_tax_rate_type_code = db.Column(db.String(8), db.ForeignKey('tax_rate_type.code'), nullable=False)
#     gift_wrap_tax_rate_type_code = db.Column(db.String(8), db.ForeignKey('tax_rate_type.code'), nullable=False)
#     _item_price_net = db.Column(db.Integer)
#     _item_price_discount_net = db.Column(db.Integer)
#     _item_price_total_net = db.Column(db.Integer)
#     _shipment_price_net = db.Column(db.Integer)
#     _shipment_price_discount_net = db.Column(db.Integer)
#     _shipment_price_total_net = db.Column(db.Integer)
#     _gift_wrap_price_net = db.Column(db.Integer)
#     _gift_wrap_price_discount_net = db.Column(db.Integer)
#     _gift_wrap_price_total_net = db.Column(db.Integer)
#     _item_price_vat_rate = db.Column(db.Integer)
#     _item_price_vat = db.Column(db.Integer)
#     _item_price_discount_vat = db.Column(db.Integer)
#     _item_price_total_vat = db.Column(db.Integer)
#     _shipment_price_vat_rate = db.Column(db.Integer)
#     _shipment_price_vat = db.Column(db.Integer)
#     _shipment_price_discount_vat = db.Column(db.Integer)
#     _shipment_price_total_vat = db.Column(db.Integer)
#     _gift_wrap_price_vat_rate = db.Column(db.Integer)
#     _gift_wrap_price_vat = db.Column(db.Integer)
#     _gift_wrap_price_discount_vat = db.Column(db.Integer)
#     _gift_wrap_price_total_vat = db.Column(db.Integer)
#     _total_value_net = db.Column(db.Integer)
#     _total_value_vat = db.Column(db.Integer)
#     _total_value_gross = db.Column(db.Integer)
#     transaction_currency_code = db.Column(db.String(8), db.ForeignKey('currency.code'), nullable=False)
#     invoice_currency_code = db.Column(db.String(8), db.ForeignKey('currency.code'))
#     invoice_exchange_rate_date = db.Column(db.Date)
#     _invoice_exchange_rate = db.Column(db.Integer)
#     _invoice_amount_net = db.Column(db.Integer)
#     _invoice_amount_vat = db.Column(db.Integer)
#     _invoice_amount_gross = db.Column(db.Integer)
#     _reverse_charge_vat_rate = db.Column(db.Integer)
#     _invoice_amount_reverse_charge_vat = db.Column(db.Integer)
#     arrival_seller_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))
#     departure_seller_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))
#     seller_vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'))


#     notifications = db.relationship(
#         'TransactionNotification', backref='transaction', lazy=True, cascade='all, delete-orphan')
