<template>
    <div>
        <b-tabs content-class="mt-3">
            <b-tab title="Total" active>
                <b-card
                    v-if="seller_firm.len_transaction_inputs === 0"
                    sub-title="An Overview Of Transactions Will Appear Here Once You Start Uploading Data"
                    class="text-center py-5"
                >
                </b-card>
            </b-tab>
            <b-tab v-for="account in seller_firm.accounts" :key="account.public_id" :title="account.channel_code" lazy>
                <table-transactions-account :channelCode="account.channel_code" />
                <!-- {{ account.channel_code }} -->
            </b-tab>
        </b-tabs>
    </div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name:'OverviewTransactions',

        computed: {
            ...mapState({
                seller_firm: state => state.seller_firm.seller_firm
            })
        }
    }
</script>

<style>
</style>
