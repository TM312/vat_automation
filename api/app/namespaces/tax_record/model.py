from datetime import datetime, date
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property


from app.extensions import db
from ..utils.ATs import tax_record_transaction_AT  # , tax_record_user_AT



class TaxRecord(db.Model):
    """ Tax Record model """
    __tablename__ = 'tax_record'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)
    created_on = db.Column(db.Date, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # downloaded_by_users = db.relationship('User', secondary=tax_record_user_AT, back_populates='downloaded_tax_records')
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    tax_jurisdiction_code = db.Column(db.String(8), db.ForeignKey('country.code'), nullable=False)
    _total_local_sale = db.Column(db.Integer, default=0)
    _total_local_sale_reverse_charge = db.Column(db.Integer, default=0)
    _total_distance_sale = db.Column(db.Integer, default=0)
    _total_non_taxable_distance_sale = db.Column(db.Integer, default=0)
    _total_intra_community_sale = db.Column(db.Integer, default=0)
    _total_export = db.Column(db.Integer, default=0)
    _total_local_acquisition = db.Column(db.Integer, default=0)
    _total_intra_community_acquisition = db.Column(db.Integer, default=0)
    _total_import = db.Column(db.Integer, default=0)

    transactions = db.relationship('Transaction', secondary=tax_record_transaction_AT, back_populates='tax_records')


    def __repr__(self):
        return '<SellerFirm: {} | validity: {}-{}>'.format(self.seller_firm.name, str(self.start_date), str(self.end_date))

    #cent values
    @hybrid_property
    def total_local_sale(self):
        return self._total_local_sale / 100

    @total_local_sale.setter
    def total_local_sale(self, value):
        self._total_local_sale = int(value * 100) if value is not None else None

    @hybrid_property
    def total_local_sale_reverse_charge(self):
        return self._total_local_sale_reverse_charge / 100

    @total_local_sale_reverse_charge.setter
    def total_local_sale_reverse_charge(self, value):
        self._total_local_sale_reverse_charge = int(value * 100) if value is not None else None

    @hybrid_property
    def total_distance_sale(self):
        return self._total_distance_sale / 100

    @total_distance_sale.setter
    def total_distance_sale(self, value):
        self._total_distance_sale = int(value * 100) if value is not None else None

    @hybrid_property
    def total_non_taxable_distance_sale(self):
        return self._total_non_taxable_distance_sale / 100

    @total_non_taxable_distance_sale.setter
    def total_non_taxable_distance_sale(self, value):
        self._total_non_taxable_distance_sale = int(value * 100) if value is not None else None

    @hybrid_property
    def total_intra_community_sale(self):
        return self._total_intra_community_sale / 100

    @total_intra_community_sale.setter
    def total_intra_community_sale(self, value):
        self._total_intra_community_sale = int(value * 100) if value is not None else None

    @hybrid_property
    def total_export(self):
        return self._total_export / 100

    @total_export.setter
    def total_export(self, value):
        self._total_export = int(value * 100) if value is not None else None

    #cent values
    @hybrid_property
    def total_local_acquisition(self):
        return self._total_local_acquisition / 100

    @total_local_acquisition.setter
    def total_local_acquisition(self, value):
        self._total_local_acquisition = int(value * 100) if value is not None else None

    #cent values
    @hybrid_property
    def total_intra_community_acquisition(self):
        return self._total_intra_community_acquisition / 100

    @total_intra_community_acquisition.setter
    def total_intra_community_acquisition(self, value):
        self._total_intra_community_acquisition = int(value * 100) if value is not None else None

    #cent values
    @hybrid_property
    def total_import(self):
        return self._total_import / 100

    @total_import.setter
    def total_import(self, value):
        self._total_import = int(value * 100) if value is not None else None
