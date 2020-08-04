<template>
    <div>
        <b-row align-h="start">
            <b-col cols="auto"><container-route-back /></b-col>
            <b-col v-if="$fetchState.pending && (taxRecord.public_id != $route.params.public_id || taxRecord.length == 0)"></b-col>
            <b-col v-else><h3 class="text-muted text-center">{{ sellerFirm.name }}</h3></b-col>
        </b-row>
        <hr>
        <card-tax-record-loading v-if="$fetchState.pending && (taxRecord.public_id != $route.params.public_id || taxRecord.length == 0)" />
        <card-tax-record v-else />

        <b-card v-if="$fetchState.pending && (taxRecord.public_id != $route.params.public_id || taxRecord.length == 0)" ></b-card>
        <table-transactions v-else class="my-5 cols-6 cols-md-12" :transactions="taxRecord.transactions"/>



    </div>

</template>

<script>
import { mapState } from 'vuex'

export default {
    layout: 'tax',
    middleware: "auth-tax",

    async fetch() {
        const { store } = this.$nuxt.context
        await store.dispatch('tax_record/get_by_public_id', this.$route.params.public_id);
        if (this.sellerFirm.length == 0 || this.taxRecord.seller_firm_public_id !== this.sellerFirm.public_id) {
            await store.dispatch('seller_firm/get_by_public_id', this.taxRecord.seller_firm_public_id)
        }

    },

    computed: {
        ...mapState({
            taxRecord: state => state.tax_record.tax_record,
            sellerFirm: state => state.seller_firm.seller_firm
        }),
    }

}
</script>

<style></style>
