<template>
    <div>
        <p>Create New</p>
            <form-add-seller-firm-tax-record />
        <hr>
        <b-row cols="3" md="4">
            <card-tax-record v-for="(tax_record, i) in tax_records" :key="i" :tax_record="tax_record" />
        </b-row>
    </div>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name:'OverviewTaxRecords',

        props: {
            business: {
                type: [Array, Object],
                required: true
            }
        },

        computed: {
            ...mapState({
                tax_records: state => state.seller_firm.seller_firm.tax_records
            }),
        }
    }
</script>

<style>
</style>
