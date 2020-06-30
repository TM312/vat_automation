<template>
    <b-tabs content-class="mt-3">
        <b-tab title="All Tax Records" active>
            <b-row cols="3" md="4">
                <card-tax-record v-for="(tax_record, i) in tax_records" :key="i" :tax_record="tax_record" />
            </b-row>
        </b-tab>
        <b-tab title="Generate New Tax Record">
            <p>tbd</p>
        </b-tab>
    </b-tabs>
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
