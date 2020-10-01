import AccountRepository from './AccountRepository'
import AccountingFirmRepository from './AccountingFirmRepository'
import AdminRepository from './AdminRepository'
import BundleRepository from './BundleRepository'
import BusinessRepository from './BusinessRepository'
import ChannelRepository from './ChannelRepository'
import CountryRepository from './CountryRepository'
import CurrencyRepository from './CurrencyRepository'
import DistanceSaleRepository from './DistanceSaleRepository'
import ExchangeRateRepository from './ExchangeRateRepository'
import ItemRepository from './ItemRepository'
import PlatformRepository from './PlatformRepository'
import SellerRepository from './SellerRepository'
import SellerFirmRepository from './SellerFirmRepository'
import StatusRepository from './StatusRepository'
import TaxAuditorRepository from './TaxAuditorRepository'
import TaxCodeRepository from './TaxCodeRepository'
import TaxRateTypeRepository from './TaxRateTypeRepository'
import TaxRecordRepository from './TaxRecordRepository'
import TaxTreatmentRepository from './TaxTreatmentRepository'
import TransactionRepository from './TransactionRepository'
import TransactionInputRepository from './TransactionInputRepository'
import UserRepository from './UserRepository'
import UtilsRepository from './UtilsRepository'
import VatRepository from './VatRepository'
import VATINRepository from './VATINRepository'

export default ($axios) => ({
    account: AccountRepository($axios),
    accounting_firm: AccountingFirmRepository($axios),
    admin: AdminRepository($axios),
    bundle: BundleRepository($axios),
    business: BusinessRepository($axios),
    channel: ChannelRepository($axios),
    country: CountryRepository($axios),
    currency: CurrencyRepository($axios),
    distance_sale: DistanceSaleRepository($axios),
    exchange_rate: ExchangeRateRepository($axios),
    item: ItemRepository($axios),
    platform: PlatformRepository($axios),
    seller: SellerRepository($axios),
    seller_firm: SellerFirmRepository($axios),
    status: StatusRepository($axios),
    tax_auditor: TaxAuditorRepository($axios),
    tax_code: TaxCodeRepository($axios),
    tax_rate_type: TaxRateTypeRepository($axios),
    tax_record: TaxRecordRepository($axios),
    tax_treatment: TaxTreatmentRepository($axios),
    transaction: TransactionRepository($axios),
    transaction_input: TransactionInputRepository($axios),
    user: UserRepository($axios),
    utils: UtilsRepository($axios),
    vat: VatRepository($axios),
    vatin: VATINRepository($axios)
})
