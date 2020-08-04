<template>
    <div>
        <b-card>
            <b-card-title>{{ taxJurisdiction.name }}</b-card-title>
            <b-card-sub-title>{{ $dateFns.format(taxRecord.start_date, 'MMMM dd, yyyy') }} – {{ $dateFns.format(taxRecord.end_date, 'MMMM dd, yyyy') }}</b-card-sub-title>
            <b-card-text>
                <b>Total Local Sale:</b> {{ Number.parseFloat(taxRecord.total_local_sale).toFixed(2) }} {{ taxJurisdiction.currency_code }} <br>
                <b>Total Local Sale_reverse_charge:</b> {{ Number.parseFloat(taxRecord.total_local_sale_reverse_charge).toFixed(2) }} {{ taxJurisdiction.currency_code }} <br>
                <b>Total Distance Sale:</b> {{ Number.parseFloat(taxRecord.total_distance_sale).toFixed(2) }} {{ taxJurisdiction.currency_code }} <br>
                <b>Total Non Taxable Distance Sale:</b> {{ Number.parseFloat(taxRecord.total_non_taxable_distance_sale).toFixed(2) }} {{ taxJurisdiction.currency_code }} <br>
                <b>Total Intra Community Sale:</b> {{ Number.parseFloat(taxRecord.total_intra_community_sale).toFixed(2) }} {{ taxJurisdiction.currency_code }} <br>
                <b>Total Export:</b> {{ Number.parseFloat(taxRecord.total_export).toFixed(2) }} {{ taxJurisdiction.currency_code }} <br>
                <b>Total Local Acquisition:</b> {{ Number.parseFloat(taxRecord.total_local_acquisition).toFixed(2) }} {{ taxJurisdiction.currency_code }} <br>
                <b>Total Intra Community Acquisition:</b> {{ Number.parseFloat(taxRecord.total_intra_community_acquisition).toFixed(2) }} {{ taxJurisdiction.currency_code }} <br>
                <b>Total Import:</b> {{ Number.parseFloat(taxRecord.total_import).toFixed(2) }} {{ taxJurisdiction.currency_code }} <br>
            </b-card-text>

        </b-card>
        <br>
        <hr>
        <br>

    </div>
</template>

<script>
import { mapState } from "vuex";

export default {
    name: 'CardTaxRecord',

    computed: {
        ...mapState({
            taxRecord: state => state.tax_record.tax_record,
            countries: state => state.country.countries,
            currencies: state => state.currency.currencies
        }),


        taxJurisdiction() {
            return this.countries.find(country => country.code == this.taxRecord.tax_jurisdiction_code)
        },

    }


}
</script>

<style>

</style>
