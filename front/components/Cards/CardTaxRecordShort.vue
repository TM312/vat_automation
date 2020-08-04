<template>
    <b-col cols="4" md="3">
        <p>"Test"</p>
        <b-card :title="tax_record.seller_firm" border-variant="success">
            <b-card-text>
                <b>Period: </b>{{ $dateFns.format(tax_record.start_date, 'MMMM dd, yyyy') }} – {{ $dateFns.format(tax_record.end_date, 'MMMM dd, yyyy') }} <br>
                <b>Tax Jurisdiction: </b>{{ taxJurisdictionName }} <br>
                <nuxt-link :to="`/tax/tax_records/${tax_record.public_id}`">Details</nuxt-link>
            </b-card-text>
        </b-card>
    </b-col>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: 'CardTaxRecordShort',
        // eslint-disable-next-line
        props: { tax_record: { type: [Array, Object] } },

        computed: {
            ...mapState({
                countries: state => state.country.countries
            }),

            taxJurisdictionName() {
                if (this.countries.length !== 0) {
                    return this.countries.find(country => country.code == this.tax_record.tax_jurisdiction_code).name
                } else {
                    return null
                }
            }
        },
    }
</script>
