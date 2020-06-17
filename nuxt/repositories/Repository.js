import TaxAuditorRepository from '~/repositories/TaxAuditorRepository'


export default ($axios) => ({
    tax_auditor: TaxAuditorRepository($axios),
})
