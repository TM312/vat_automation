<template>
    <div>
        <container-route-back />
        <b-container fluid>
             <b-alert :show="!$fetchState.pending && transactionInput.length != 0" :variant="transactionInput.processed ? 'info' : 'danger'">
                <p v-if="transactionInput.processed">The transaction has been successfully processed on {{ new Date(transactionInput.processed_on).toLocaleString() }} </p>
                <p v-else>The transaction has not been processed yet due to network errors. Click here to retry: <button-validate-transaction-input :transactionInputPublicId="transactionInput.public_id"/> </p>
            </b-alert>
            <card-transaction-input class="mb-5"/>
            <hr>
            <h2>Tax Related Processes</h2>

            <view-transactions v-if="!$fetchState.pending && transactionInput.length != 0" class="my-5 cols-6 cols-md-12" :transactions="transactionInput.transactions" />
            <hr>
            <h2>Transaction Bundle</h2>
            <p class="text-muted">Below you find a list of all related transactions.</p>
            <table-transaction-input-bundle v-if="!$fetchState.pending && transactionInput.length != 0" :bundlePublicId="transactionInput.bundle_public_id"/>

        </b-container>
    </div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        layout: "tax",
        middleware: "auth-tax",

        async fetch() {
            const { store } = this.$nuxt.context
            await store.dispatch('transaction_input/get_by_public_id', this.$route.params.public_id);

        },

        computed: {
            ...mapState({
                transactionInput: state => state.transaction_input.transaction_input,
            })
        }
    };
</script>

<style></style>
