<template>
    <div>
        <b-tabs pills content-class="mt-3">
            <b-tab title="Total" active>
                <b-card
                    v-if="transaction_inputs.length === 0"
                    sub-title="An Overview Of Transactions Will Appear Here Once You Start Uploading Data"
                    class="text-center py-5"
                ></b-card>
                <table-transaction-inputs v-else />

            </b-tab>
            <b-tab v-for="account in seller_firm.accounts" :key="account.public_id" :title="account.channel_code" lazy>
                <lazy-table-transaction-inputs :channelCode="account.channel_code" />
                <!-- {{ account.channel_code }} -->
            </b-tab>
        </b-tabs>
    </div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name:'OverviewTransactionInputs',

        async fetch() {
            const { store } = this.$nuxt.context;
            await store.dispatch("transaction_input/get_by_seller_firm_public_id", this.$route.params.public_id);
        },

        computed: {
            ...mapState({
                seller_firm: state => state.seller_firm.seller_firm,
                transaction_inputs: state => state.transaction_input.transaction_inputs
            }),
        }
    }
</script>

<style>
</style>
