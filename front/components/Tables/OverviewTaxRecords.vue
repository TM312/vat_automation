<template>
    <div>
        <b-button v-b-toggle.collapse-tax-record-form variant="outline-primary">Create New</b-button>
            <b-collapse id="collapse-tax-record-form" class="mt-2">
                <form-add-seller-firm-tax-record />
            </b-collapse>
        <hr>
        <b-row class="mb-3" cols="1" cols-md="2" cols-xl="4">
            <b-col v-for="(taxRecord, i) in taxRecords" :key="i" class="mb-2">
                <card-tax-record-short :taxRecord="taxRecord" />
            </b-col>
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
                taxRecords: state => state.seller_firm.seller_firm.tax_records
            }),
        }
    }
</script>

<style>
</style>
