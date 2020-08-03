<template>
    <div>
        <b-button v-b-toggle.collapse-tax-record-form variant="outline-primary">Create New</b-button>
            <b-collapse id="collapse-tax-record-form" class="mt-2">
                <form-add-seller-firm-tax-record />
            </b-collapse>
        <hr>
        <card-tax-record-short v-for="(tax_record, i) in tax_records" :key="i" :tax_record="tax_record" />
    </div>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name:'OverviewTaxRecords',

        // data() {
        //     return {
        //         buttonPressed: false
        //     }
        // },

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
