<template>
    <b-col cols="4" md="3">
        <b-card :title="taxRecord.seller_firm" border-variant="success">
            <b-card-text>
                <b>Period: </b>{{ $dateFns.format(taxRecord.start_date, 'MMMM dd, yyyy') }} – {{ $dateFns.format(taxRecord.end_date, 'MMMM dd, yyyy') }} <br>
                <b>Tax Jurisdiction: </b>{{ taxJurisdictionName }} <br><br>
                <b>Taxable Turnover Amount:</b>{{ Number.parseFloat(taxRecord.taxable_turnover_amount).toFixed(2) }} {{ taxRecord.currency_code }}<br>
                <b>Payable Vat Amount:</b>{{ Number.parseFloat(taxRecord.taxable_turnover_amount).toFixed(2) }} {{ taxRecord.currency_code }}<br><br>
                <nuxt-link :to="`/tax/tax_records/${taxRecord.public_id}`">Details</nuxt-link>
            </b-card-text>
        </b-card>
    </b-col>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: 'CardTaxRecordShort',
        // eslint-disable-next-line
        props: { taxRecord: { type: [Array, Object] } },

        computed: {
            ...mapState({
                countries: state => state.country.countries
            }),

            taxJurisdictionName() {
                if (this.countries.length !== 0) {
                    return this.countries.find(country => country.code == this.taxRecord.tax_jurisdiction_code).name
                } else {
                    return null
                }
            }
        },
    }
</script>
