from app.namespaces.business.accounting_firm import AccountingFirm
from app.namespaces.business.seller_firm import SellerFirm
from app.namespaces.business.seller_firm.service import SellerFirmService
from app.namespaces.user.tax_auditor import TaxAuditor
from app.namespaces.distance_sale.service import DistanceSaleService
from app.extensions import db

class SellerFirmSeedService:

    @staticmethod
    def seed_sample_seller_firm():

        sample_seller_firm = SellerFirm(
            name='Bond Store Ltd',
            address="37–38 St James's Street, London",
            establishment_country_code='GB'
        )
        db.session.add(sample_seller_firm)
        db.session.commit()

        bondSF = SellerFirmService.get_by_name_establishment_country(seller_firm_name='Bond Store Ltd', establishment_country_code='GB')

        # create deactivated distance sales for seller firm
        DistanceSaleService.create_inactive_ds_from_thresholds(bondSF.id)



    @staticmethod
    def append_accounting_firm_to_seller_firm():
        accounting_firm_bond = AccountingFirm.query.filter_by(name='Accounting Firm Bond').first()
        bondSF = SellerFirmService.get_by_name_establishment_country(seller_firm_name='Bond Store Ltd', establishment_country_code='GB')

        if not isinstance(accounting_firm_bond, AccountingFirm):
            raise
        accounting_firm_bond.clients.append(bondSF)
        db.session.commit()

        m_auditor = TaxAuditor.query.filter_by(name='M').first()
        if not isinstance(m_auditor, TaxAuditor):
            raise
        m_auditor.key_accounts.append(bondSF)
        db.session.commit()
