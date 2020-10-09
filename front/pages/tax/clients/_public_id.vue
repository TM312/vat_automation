<template>
    <div>
        <b-row align-h="start">
            <b-col cols="auto"><container-route-back /></b-col>
            <b-col><h3 class="text-muted text-center">{{ sellerFirm.name }}</h3></b-col>
        </b-row>
        <hr>
        <b-container fluid>
            <b-tabs pills card vertical>
                <b-tab title='Company' active>
                    <overview-base-data-loading v-if="$fetchState.pending && (sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0)" />
                    <overview-base-data v-else />
                </b-tab>

                <b-tab title='Items' :disabled="$fetchState.pending && sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0" lazy>
                    <span v-if="$fetchState.pending && (sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0)"></span>
                    <lazy-card-items v-else />
                </b-tab>

                <b-tab title='Transactions' :disabled="$fetchState.pending && sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0" lazy>
                    <span v-if="$fetchState.pending && (sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0)"></span>
                    <lazy-overview-transaction-inputs v-else />
                </b-tab>

                <b-tab title='Tax Records' :disabled="$fetchState.pending && sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0" lazy>
                    <span v-if="$fetchState.pending && (sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0)"></span>
                    <lazy-overview-tax-records v-else />
                </b-tab>

                <b-tab title='Upload Files' :disabled="$fetchState.pending && sellerFirm.public_id != $route.params.public_id || sellerFirm.length === 0" title-link-class="text-info" lazy>
                    <lazy-add-data-files :seller_firm_public_id="sellerFirm.public_id" />
                </b-tab>

            </b-tabs>
        </b-container>

        <toasts-static-data-upload />

        <toast-new-tax-record />

    </div>
</template>

<script>
    import { mapState } from 'vuex'
    export default {
        layout: "tax",

        async fetch() {
            const { store } = this.$nuxt.context
            if (this.sellerFirm.length == 0 || this.sellerFirm.public_id !== this.$route.params.public_id) {
                await store.dispatch('seller_firm/get_by_public_id', this.$route.params.public_id)
            }
        },

        computed: {
            ...mapState({
                sellerFirm: state => state.seller_firm.seller_firm
            })
        },

        beforeDestroy() {
            this.resetStoreSellerFirm()
        },

        methods: {
            resetStoreSellerFirm() {
                const { store } = this.$nuxt.context
                store.dispatch('status/clear_all')
                // store.dispatch('seller_firm/clear_seller_firm')
                // store.dispatch('transaction_input/clear_transaction_inputs')
                store.dispatch('tax_record/clear_tax_records')

            }

        },
    };
</script>

<style></style>
