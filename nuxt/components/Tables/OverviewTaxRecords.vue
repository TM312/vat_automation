<template>
    <b-tabs content-class="mt-3">
        <b-tab title="All Tax Records" active>
            <b-row cols="3" md="4">
                <card-tax-record v-for="(client_tax_record, i) in client_tax_records" :key="i" :tax_record="tax_record" />
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

        computed: {
            ...mapState({
                client_seller_firms: state => state.seller_firm.client_seller_firms
            }),
        }
    }
</script>

<style>
</style>
