<template>
    <div>

        <b-row align-h="start">
            <b-col cols="auto"><container-route-back /></b-col>
            <b-col><h3 class="text-muted text-center">{{ sellerFirm.name }}</h3></b-col>
        </b-row>
        <hr>
        <b-container fluid>
             <b-alert :show="!transactionInput.processed && !$fetchState.pending" variant="danger">
                <p>The transaction has not been processed yet due to network errors. Click here to retry: <button-validate-transaction-input :transactionInputPublicId="$route.params.public_id"/> </p>
            </b-alert>
            <b-tabs pills card vertical>
                <b-tab title='Input File' active>
                    <overview-base-data-loading v-if="$fetchState.pending || transactionInput.length === 0" />
                    <card-transaction-input v-else id="file"/>

                    <b-card title="Transaction Bundle" sub-title="A list of all related transactions" class="mt-4">
                        <span v-if="$fetchState.pending || transactionInput.length === 0"></span>
                        <table-transaction-inputs v-else :transactionInputs="transactionInputsBundle" class="mt-4"/>
                    </b-card>

                </b-tab>

                <b-tab title='Tax Processes' lazy :disabled="$fetchState.pending && sellerFirm.public_id != $route.params.public_id || transactionInput.length === 0">
                    <span v-if="$fetchState.pending || transactionInput.length === 0"></span>
                    <view-transactions v-else :transactions="transactionInput.transactions" />

                    <b-card title="Transaction Bundle" sub-title="A list of all related transactions" class="mt-4">
                        <span v-if="$fetchState.pending || transactionInput.length === 0"></span>
                        <table-transaction-inputs v-else :transactionInputs="transactionInputsBundle"/>
                    </b-card>

                </b-tab>


            </b-tabs>
        </b-container>

    </div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        layout: "tax",
        middleware: "auth-tax",

        data() {
            return {
                fileCollapse: true,
                bundleCollapse: true,
                taxCollapse: true
            }
        },

        async fetch() {
            const { store } = this.$nuxt.context
            await store.dispatch('transaction_input/get_by_public_id', this.$route.params.public_id);
            // if (this.transactionInput.length == 0) {
            //     await store.dispatch('seller_firm/get_by_public_id', this.transactionInput.seller_firm_public_id)
            // }
        },


// async fetch() {
//         if (this.transactionInputsBundle.length === 0) {
//             const { store } = this.$nuxt.context;
//             await store.dispatch("transaction_input/get_by_bundle_public_id", this.bundlePublicId);
//         }
//     },

    // computed: {
    //     ...mapState({
    //         transactionInputsBundle: state => state.transaction_input.transaction_inputs_bundle
    //     })
    // }


        computed: {
            ...mapState({
                transactionInput: state => state.transaction_input.transaction_input,
                transactionInputsBundle: state => state.transaction_input.transaction_inputs_bundle,
                sellerFirm: state => state.seller_firm.seller_firm
            }),

            iconCollapseFile() {
                return this.fileCollapse ? 'arrows-angle-contract' : 'arrows-angle-expand'
            },
            iconCollapseBundle() {
                return this.bundleCollapse ? 'arrows-angle-contract' : 'arrows-angle-expand'
            },
            iconCollapseTax() {
                return this.taxCollapse ? 'arrows-angle-contract' : 'arrows-angle-expand'
            }
        },

        beforeDestroy() {
            this.clearStoreTransactionInputs()
        },

        methods: {
            clearStoreTransactionInputs() {
                const { store } = this.$nuxt.context
                store.dispatch('transaction_input/clear_transaction_inputs_bundle')
            }

        },


    };
</script>

<style></style>
