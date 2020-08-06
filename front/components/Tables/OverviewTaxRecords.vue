<template>
    <div>
        <b-button v-b-toggle.collapse-tax-record-form variant="outline-primary">Create New</b-button>
            <b-collapse id="collapse-tax-record-form" class="mt-2">
                <form-add-seller-firm-tax-record />
            </b-collapse>
        <hr>
        <card-tax-record-short v-for="(taxRecord, i) in taxRecords" :key="i" :taxRecord="taxRecord" />
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
                taxRecords: state => state.seller_firm.seller_firm.taxRecords
            }),
        }
    }
</script>

<style>
</style>
