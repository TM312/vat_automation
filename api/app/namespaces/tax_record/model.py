from datetime import datetime, date
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property


from app.extensions import db
from app.namespaces.utils.ATs import tax_record_transaction_AT  # , tax_record_user_AT



class TaxRecord(db.Model):
    """ Tax Record model """
    __tablename__ = 'tax_record'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)
    created_on = db.Column(db.Date, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    filename = db.Column(db.String(128), nullable=False)

    # downloaded_by_users = db.relationship('User', secondary=tax_record_user_AT, back_populates='downloaded_tax_records')
    seller_firm_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    tax_jurisdiction_code = db.Column(db.String(8), db.ForeignKey('country.code'), nullable=False)
    currency_code = db.Column(db.String(8), db.ForeignKey('currency.code'), nullable=False)

    vatin_id = db.Column(db.Integer, db.ForeignKey('vatin.id'), nullable=False)


    _local_sales_sales_net = db.Column(db.Integer, default=0)
    _local_sales_refunds_net = db.Column(db.Integer, default=0)
    _local_sales_total_net = db.Column(db.Integer, default=0)
    _local_sales_sales_vat = db.Column(db.Integer, default=0)
    _local_sales_refunds_vat = db.Column(db.Integer, default=0)
    _local_sales_total_vat = db.Column(db.Integer, default=0)
    _local_sales_sales_gross = db.Column(db.Integer, default=0)
    _local_sales_refunds_gross = db.Column(db.Integer, default=0)
    _local_sales_total_gross = db.Column(db.Integer, default=0)

    _local_sale_reverse_charges_sales_net = db.Column(db.Integer, default=0)
    _local_sale_reverse_charges_refunds_net = db.Column(db.Integer, default=0)
    _local_sale_reverse_charges_total_net = db.Column(db.Integer, default=0)
    _local_sale_reverse_charges_sales_vat = db.Column(db.Integer, default=0)
    _local_sale_reverse_charges_refunds_vat = db.Column(db.Integer, default=0)
    _local_sale_reverse_charges_total_vat = db.Column(db.Integer, default=0)
    _local_sale_reverse_charges_sales_gross = db.Column(db.Integer, default=0)
    _local_sale_reverse_charges_refunds_gross = db.Column(db.Integer, default=0)
    _local_sale_reverse_charges_total_gross = db.Column(db.Integer, default=0)

    _distance_sales_sales_net = db.Column(db.Integer, default=0)
    _distance_sales_refunds_net = db.Column(db.Integer, default=0)
    _distance_sales_total_net = db.Column(db.Integer, default=0)
    _distance_sales_sales_vat = db.Column(db.Integer, default=0)
    _distance_sales_refunds_vat = db.Column(db.Integer, default=0)
    _distance_sales_total_vat = db.Column(db.Integer, default=0)
    _distance_sales_sales_gross = db.Column(db.Integer, default=0)
    _distance_sales_refunds_gross = db.Column(db.Integer, default=0)
    _distance_sales_total_gross = db.Column(db.Integer, default=0)

    _non_taxable_distance_sales_sales_net = db.Column(db.Integer, default=0)
    _non_taxable_distance_sales_refunds_net = db.Column(db.Integer, default=0)
    _non_taxable_distance_sales_total_net = db.Column(db.Integer, default=0)
    _non_taxable_distance_sales_sales_vat = db.Column(db.Integer, default=0)
    _non_taxable_distance_sales_refunds_vat = db.Column(db.Integer, default=0)
    _non_taxable_distance_sales_total_vat = db.Column(db.Integer, default=0)
    _non_taxable_distance_sales_sales_gross = db.Column(db.Integer, default=0)
    _non_taxable_distance_sales_refunds_gross = db.Column(db.Integer, default=0)
    _non_taxable_distance_sales_total_gross = db.Column(db.Integer, default=0)

    _intra_community_sales_sales_net = db.Column(db.Integer, default=0)
    _intra_community_sales_refunds_net = db.Column(db.Integer, default=0)
    _intra_community_sales_total_net = db.Column(db.Integer, default=0)

    _exports_sales_net = db.Column(db.Integer, default=0)
    _exports_refunds_net = db.Column(db.Integer, default=0)
    _exports_total_net = db.Column(db.Integer, default=0)

    _ica_acquisitions_net = db.Column(db.Integer, default=0)
    _ica_refunds_net = db.Column(db.Integer, default=0)
    _ica_total_net = db.Column(db.Integer, default=0)

    _ica_acquisitions_reverse_charge_vat = db.Column(db.Integer, default=0)
    _ica_refunds_reverse_charge_vat = db.Column(db.Integer, default=0)
    _ica_total_reverse_charge_vat = db.Column(db.Integer, default=0)

    _local_acquisitions_acquisitions_net = db.Column(db.Integer, default=0)
    _local_acquisitions_refunds_net = db.Column(db.Integer, default=0)
    _local_acquisitions_total_net = db.Column(db.Integer, default=0)
    _local_acquisitions_acquisitions_vat = db.Column(db.Integer, default=0)
    _local_acquisitions_refunds_vat = db.Column(db.Integer, default=0)
    _local_acquisitions_total_vat = db.Column(db.Integer, default=0)
    _local_acquisitions_acquisitions_gross = db.Column(db.Integer, default=0)
    _local_acquisitions_refunds_gross = db.Column(db.Integer, default=0)
    _local_acquisitions_total_gross = db.Column(db.Integer, default=0)

    _taxable_turnover_amount = db.Column(db.Integer, default=0)
    _payable_vat_amount = db.Column(db.Integer, default=0)


    transactions = db.relationship('Transaction', secondary=tax_record_transaction_AT, back_populates='tax_records')


    def __repr__(self):
        return '<SellerFirm: {} | validity: {}-{}>'.format(self.seller_firm.name, str(self.start_date), str(self.end_date))


    #cent values
    @hybrid_property
    def local_sales_sales_net(self):
        return self._local_sales_sales_net / 100

    @local_sales_sales_net.setter
    def local_sales_sales_net(self, value):
        self._local_sales_sales_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sales_refunds_net(self):
        return self._local_sales_refunds_net / 100

    @local_sales_refunds_net.setter
    def local_sales_refunds_net(self, value):
        self._local_sales_refunds_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sales_total_net(self):
        return self._local_sales_total_net / 100

    @local_sales_total_net.setter
    def local_sales_total_net(self, value):
        self._local_sales_total_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sales_sales_vat(self):
        return self._local_sales_sales_vat / 100

    @local_sales_sales_vat.setter
    def local_sales_sales_vat(self, value):
        self._local_sales_sales_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sales_refunds_vat(self):
        return self._local_sales_refunds_vat / 100

    @local_sales_refunds_vat.setter
    def local_sales_refunds_vat(self, value):
        self._local_sales_refunds_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sales_total_vat(self):
        return self._local_sales_total_vat / 100

    @local_sales_total_vat.setter
    def local_sales_total_vat(self, value):
        self._local_sales_total_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sales_sales_gross(self):
        return self._local_sales_sales_gross / 100

    @local_sales_sales_gross.setter
    def local_sales_sales_gross(self, value):
        self._local_sales_sales_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sales_refunds_gross(self):
        return self._local_sales_refunds_gross / 100

    @local_sales_refunds_gross.setter
    def local_sales_refunds_gross(self, value):
        self._local_sales_refunds_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sales_total_gross(self):
        return self._local_sales_total_gross / 100

    @local_sales_total_gross.setter
    def local_sales_total_gross(self, value):
        self._local_sales_total_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sale_reverse_charges_sales_net(self):
        return self._local_sale_reverse_charges_sales_net / 100

    @local_sale_reverse_charges_sales_net.setter
    def local_sale_reverse_charges_sales_net(self, value):
        self._local_sale_reverse_charges_sales_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sale_reverse_charges_refunds_net(self):
        return self._local_sale_reverse_charges_refunds_net / 100

    @local_sale_reverse_charges_refunds_net.setter
    def local_sale_reverse_charges_refunds_net(self, value):
        self._local_sale_reverse_charges_refunds_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sale_reverse_charges_total_net(self):
        return self._local_sale_reverse_charges_total_net / 100

    @local_sale_reverse_charges_total_net.setter
    def local_sale_reverse_charges_total_net(self, value):
        self._local_sale_reverse_charges_total_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sale_reverse_charges_sales_vat(self):
        return self._local_sale_reverse_charges_sales_vat / 100

    @local_sale_reverse_charges_sales_vat.setter
    def local_sale_reverse_charges_sales_vat(self, value):
        self._local_sale_reverse_charges_sales_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sale_reverse_charges_refunds_vat(self):
        return self._local_sale_reverse_charges_refunds_vat / 100

    @local_sale_reverse_charges_refunds_vat.setter
    def local_sale_reverse_charges_refunds_vat(self, value):
        self._local_sale_reverse_charges_refunds_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sale_reverse_charges_total_vat(self):
        return self._local_sale_reverse_charges_total_vat / 100

    @local_sale_reverse_charges_total_vat.setter
    def local_sale_reverse_charges_total_vat(self, value):
        self._local_sale_reverse_charges_total_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sale_reverse_charges_sales_gross(self):
        return self._local_sale_reverse_charges_sales_gross / 100

    @local_sale_reverse_charges_sales_gross.setter
    def local_sale_reverse_charges_sales_gross(self, value):
        self._local_sale_reverse_charges_sales_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sale_reverse_charges_refunds_gross(self):
        return self._local_sale_reverse_charges_refunds_gross / 100

    @local_sale_reverse_charges_refunds_gross.setter
    def local_sale_reverse_charges_refunds_gross(self, value):
        self._local_sale_reverse_charges_refunds_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_sale_reverse_charges_total_gross(self):
        return self._local_sale_reverse_charges_total_gross / 100

    @local_sale_reverse_charges_total_gross.setter
    def local_sale_reverse_charges_total_gross(self, value):
        self._local_sale_reverse_charges_total_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def distance_sales_sales_net(self):
        return self._distance_sales_sales_net / 100

    @distance_sales_sales_net.setter
    def distance_sales_sales_net(self, value):
        self._distance_sales_sales_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def distance_sales_refunds_net(self):
        return self._distance_sales_refunds_net / 100

    @distance_sales_refunds_net.setter
    def distance_sales_refunds_net(self, value):
        self._distance_sales_refunds_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def distance_sales_total_net(self):
        return self._distance_sales_total_net / 100

    @distance_sales_total_net.setter
    def distance_sales_total_net(self, value):
        self._distance_sales_total_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def distance_sales_sales_vat(self):
        return self._distance_sales_sales_vat / 100

    @distance_sales_sales_vat.setter
    def distance_sales_sales_vat(self, value):
        self._distance_sales_sales_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def distance_sales_refunds_vat(self):
        return self._distance_sales_refunds_vat / 100

    @distance_sales_refunds_vat.setter
    def distance_sales_refunds_vat(self, value):
        self._distance_sales_refunds_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def distance_sales_total_vat(self):
        return self._distance_sales_total_vat / 100

    @distance_sales_total_vat.setter
    def distance_sales_total_vat(self, value):
        self._distance_sales_total_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def distance_sales_sales_gross(self):
        return self._distance_sales_sales_gross / 100

    @distance_sales_sales_gross.setter
    def distance_sales_sales_gross(self, value):
        self._distance_sales_sales_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def distance_sales_refunds_gross(self):
        return self._distance_sales_refunds_gross / 100

    @distance_sales_refunds_gross.setter
    def distance_sales_refunds_gross(self, value):
        self._distance_sales_refunds_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def distance_sales_total_gross(self):
        return self._distance_sales_total_gross / 100

    @distance_sales_total_gross.setter
    def distance_sales_total_gross(self, value):
        self._distance_sales_total_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def non_taxable_distance_sales_sales_net(self):
        return self._non_taxable_distance_sales_sales_net / 100

    @non_taxable_distance_sales_sales_net.setter
    def non_taxable_distance_sales_sales_net(self, value):
        self._non_taxable_distance_sales_sales_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def non_taxable_distance_sales_refunds_net(self):
        return self._non_taxable_distance_sales_refunds_net / 100

    @non_taxable_distance_sales_refunds_net.setter
    def non_taxable_distance_sales_refunds_net(self, value):
        self._non_taxable_distance_sales_refunds_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def non_taxable_distance_sales_total_net(self):
        return self._non_taxable_distance_sales_total_net / 100

    @non_taxable_distance_sales_total_net.setter
    def non_taxable_distance_sales_total_net(self, value):
        self._non_taxable_distance_sales_total_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def non_taxable_distance_sales_sales_vat(self):
        return self._non_taxable_distance_sales_sales_vat / 100

    @non_taxable_distance_sales_sales_vat.setter
    def non_taxable_distance_sales_sales_vat(self, value):
        self._non_taxable_distance_sales_sales_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def non_taxable_distance_sales_refunds_vat(self):
        return self._non_taxable_distance_sales_refunds_vat / 100

    @non_taxable_distance_sales_refunds_vat.setter
    def non_taxable_distance_sales_refunds_vat(self, value):
        self._non_taxable_distance_sales_refunds_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def non_taxable_distance_sales_total_vat(self):
        return self._non_taxable_distance_sales_total_vat / 100

    @non_taxable_distance_sales_total_vat.setter
    def non_taxable_distance_sales_total_vat(self, value):
        self._non_taxable_distance_sales_total_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def non_taxable_distance_sales_sales_gross(self):
        return self._non_taxable_distance_sales_sales_gross / 100

    @non_taxable_distance_sales_sales_gross.setter
    def non_taxable_distance_sales_sales_gross(self, value):
        self._non_taxable_distance_sales_sales_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def non_taxable_distance_sales_refunds_gross(self):
        return self._non_taxable_distance_sales_refunds_gross / 100

    @non_taxable_distance_sales_refunds_gross.setter
    def non_taxable_distance_sales_refunds_gross(self, value):
        self._non_taxable_distance_sales_refunds_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def non_taxable_distance_sales_total_gross(self):
        return self._non_taxable_distance_sales_total_gross / 100

    @non_taxable_distance_sales_total_gross.setter
    def non_taxable_distance_sales_total_gross(self, value):
        self._non_taxable_distance_sales_total_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def intra_community_sales_sales_net(self):
        return self._intra_community_sales_sales_net / 100

    @intra_community_sales_sales_net.setter
    def intra_community_sales_sales_net(self, value):
        self._intra_community_sales_sales_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def intra_community_sales_refunds_net(self):
        return self._intra_community_sales_refunds_net / 100

    @intra_community_sales_refunds_net.setter
    def intra_community_sales_refunds_net(self, value):
        self._intra_community_sales_refunds_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def intra_community_sales_total_net(self):
        return self._intra_community_sales_total_net / 100

    @intra_community_sales_total_net.setter
    def intra_community_sales_total_net(self, value):
        self._intra_community_sales_total_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def exports_sales_net(self):
        return self._exports_sales_net / 100

    @exports_sales_net.setter
    def exports_sales_net(self, value):
        self._exports_sales_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def exports_refunds_net(self):
        return self._exports_refunds_net / 100

    @exports_refunds_net.setter
    def exports_refunds_net(self, value):
        self._exports_refunds_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def exports_total_net(self):
        return self._exports_total_net / 100

    @exports_total_net.setter
    def exports_total_net(self, value):
        self._exports_total_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def ica_acquisitions_net(self):
        return self._ica_acquisitions_net / 100

    @ica_acquisitions_net.setter
    def ica_acquisitions_net(self, value):
        self._ica_acquisitions_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def ica_refunds_net(self):
        return self._ica_refunds_net / 100

    @ica_refunds_net.setter
    def ica_refunds_net(self, value):
        self._ica_refunds_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def ica_total_net(self):
        return self._ica_total_net / 100

    @ica_total_net.setter
    def ica_total_net(self, value):
        self._ica_total_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def ica_acquisitions_reverse_charge_vat(self):
        return self._ica_acquisitions_reverse_charge_vat / 100

    @ica_acquisitions_reverse_charge_vat.setter
    def ica_acquisitions_reverse_charge_vat(self, value):
        self._ica_acquisitions_reverse_charge_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def ica_refunds_reverse_charge_vat(self):
        return self._ica_refunds_reverse_charge_vat / 100

    @ica_refunds_reverse_charge_vat.setter
    def ica_refunds_reverse_charge_vat(self, value):
        self._ica_refunds_reverse_charge_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def ica_total_reverse_charge_vat(self):
        return self._ica_total_reverse_charge_vat / 100

    @ica_total_reverse_charge_vat.setter
    def ica_total_reverse_charge_vat(self, value):
        self._ica_total_reverse_charge_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_acquisitions_acquisitions_net(self):
        return self._local_acquisitions_acquisitions_net / 100

    @local_acquisitions_acquisitions_net.setter
    def local_acquisitions_acquisitions_net(self, value):
        self._local_acquisitions_acquisitions_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_acquisitions_refunds_net(self):
        return self._local_acquisitions_refunds_net / 100

    @local_acquisitions_refunds_net.setter
    def local_acquisitions_refunds_net(self, value):
        self._local_acquisitions_refunds_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_acquisitions_total_net(self):
        return self._local_acquisitions_total_net / 100

    @local_acquisitions_total_net.setter
    def local_acquisitions_total_net(self, value):
        self._local_acquisitions_total_net = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_acquisitions_acquisitions_vat(self):
        return self._local_acquisitions_acquisitions_vat / 100

    @local_acquisitions_acquisitions_vat.setter
    def local_acquisitions_acquisitions_vat(self, value):
        self._local_acquisitions_acquisitions_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_acquisitions_refunds_vat(self):
        return self._local_acquisitions_refunds_vat / 100

    @local_acquisitions_refunds_vat.setter
    def local_acquisitions_refunds_vat(self, value):
        self._local_acquisitions_refunds_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_acquisitions_total_vat(self):
        return self._local_acquisitions_total_vat / 100

    @local_acquisitions_total_vat.setter
    def local_acquisitions_total_vat(self, value):
        self._local_acquisitions_total_vat = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_acquisitions_acquisitions_gross(self):
        return self._local_acquisitions_acquisitions_gross / 100

    @local_acquisitions_acquisitions_gross.setter
    def local_acquisitions_acquisitions_gross(self, value):
        self._local_acquisitions_acquisitions_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_acquisitions_refunds_gross(self):
        return self._local_acquisitions_refunds_gross / 100

    @local_acquisitions_refunds_gross.setter
    def local_acquisitions_refunds_gross(self, value):
        self._local_acquisitions_refunds_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def local_acquisitions_total_gross(self):
        return self._local_acquisitions_total_gross / 100

    @local_acquisitions_total_gross.setter
    def local_acquisitions_total_gross(self, value):
        self._local_acquisitions_total_gross = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def taxable_turnover_amount(self):
        return self._taxable_turnover_amount / 100

    @taxable_turnover_amount.setter
    def taxable_turnover_amount(self, value):
        self._taxable_turnover_amount = int(round(value * 100)) if value is not None else None


    @hybrid_property
    def payable_vat_amount(self):
        return self._payable_vat_amount / 100

    @payable_vat_amount.setter
    def payable_vat_amount(self, value):
        self._payable_vat_amount = int(round(value * 100)) if value is not None else None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = '{}_{}_{}_{}.csv'.format(
            kwargs.get('tax_jurisdiction_code'),
            kwargs.get('start_date'),
            kwargs.get('end_date'),
            str(uuid4())[:8]
        )
