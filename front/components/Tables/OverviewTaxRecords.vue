<template>
    <div>
        <b-button v-b-toggle.collapse-tax-record-form variant="outline-primary">Create New</b-button>
            <b-collapse id="collapse-tax-record-form" class="mt-2">
                <lazy-form-add-seller-firm-tax-record />
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

        async fetch() {
            const { store } = this.$nuxt.context
            if (this.taxRecords.length == 0) {
                await store.dispatch('tax_record/get_all_by_seller_firm_public_id', this.sellerFirm.public_id)
            }
        },

        computed: {
            ...mapState({
                sellerFirm: state => state.seller_firm.seller_firm,
                taxRecords: state => state.tax_record.tax_records
            }),
        }


    }
</script>

<style>
</style>
