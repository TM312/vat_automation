import AccountRepository from './AccountRepository'
import BundleRepository from './BundleRepository'
import BusinessRepository from './BusinessRepository'
import AccountingFirmRepository from './AccountingFirmRepository'
import CustomerFirmRepository from './CustomerFirmRepository'
import SellerFirmRepository from './SellerFirmRepository'
import ChannelRepository from './ChannelRepository'
import CountryRepository from './CountryRepository'
import CurrencyRepository from './CurrencyRepository'
import DistanceSaleRepository from './DistanceSaleRepository'
import ExchangeRateRepository from './ExchangeRateRepository'
import ItemRepository from './ItemRepository'
import PlatformRepository from './PlatformRepository'
import TaxCodeRepository from './TaxCodeRepository'
import TaxTreatmentRepository from './TaxTreatmentRepository'
import VatRepository from './VatRepository'
import VATINRepository from './VATINRepository'
import TaxRecordRepository from './TaxRecordRepository'
import TransactionRepository from './TransactionRepository'
import TransactionInputRepository from './TransactionInputRepository'
import UserRepository from './UserRepository'
import AdminRepository from './AdminRepository'
import SellerRepository from './SellerRepository'
import TaxAuditorRepository from './TaxAuditorRepository'
// import TemplateRepository from './TemplateRepository'


export default ($axios) => ({
    account: AccountRepository($axios),
    bundle: BundleRepository($axios),
    business: BusinessRepository($axios),
    accounting_firm: AccountingFirmRepository($axios),
    customer_firm: CustomerFirmRepository($axios),
    seller_firm: SellerFirmRepository($axios),
    channel: ChannelRepository($axios),
    country: CountryRepository($axios),
    currency: CurrencyRepository($axios),
    distance_sale: DistanceSaleRepository($axios),
    exchange_rate: ExchangeRateRepository($axios),
    item: ItemRepository($axios),
    platform: PlatformRepository($axios),
    tax_code: TaxCodeRepository($axios),
    tax_treatment: TaxTreatmentRepository($axios),
    vat: VatRepository($axios),
    vatin: VATINRepository($axios),
    tax_record: TaxRecordRepository($axios),
    transaction: TransactionRepository($axios),
    transaction_input: TransactionInputRepository($axios),
    user: UserRepository($axios),
    admin: AdminRepository($axios),
    seller: SellerRepository($axios),
    tax_auditor: TaxAuditorRepository($axios),
    // template: TemplateRepository($axios),
})
