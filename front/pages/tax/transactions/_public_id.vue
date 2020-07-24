<template>
    <div>
        <container-route-back />
        <b-container fluid>
            <card-transaction-input class="mb-5"/>
            <hr>
            <h2>Tax Related Processes</h2>

            <view-transactions v-if="!$fetchState.pending && transactionInput.length != 0" class="my-5 cols-6 cols-md-12" />
            <hr>
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
                transactionInput: state => state.transaction_input.transaction_input
            })
        }
    };
</script>

<style></style>
