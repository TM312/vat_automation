<template>
    <div>
        <b-button v-if="transactionInputs.length > 0" variant="outline-danger" class="align-right" :disabled="buttonDisabled" @click="removeAll">Delete All</b-button>
        <b-tabs pills content-class="mt-3">
            <b-tab title="Total" active>
                <b-card
                    v-if="transactionInputs.length === 0"
                    sub-title="An Overview Of Transactions Will Appear Here Once You Start Uploading Data"
                    class="text-center py-5"
                ></b-card>
                <table-transaction-inputs v-else />

            </b-tab>
            <b-tab v-for="account in sellerFirm.accounts" :key="account.public_id" :title="account.channel_code" lazy>
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

        data() {
            return {
                buttonDisabled: false
            }
        },

        async fetch() {
            const { store } = this.$nuxt.context;
            await store.dispatch("transaction_input/get_by_seller_firm_public_id", this.$route.params.public_id);
        },

        computed: {
            ...mapState({
                sellerFirm: state => state.seller_firm.seller_firm,
                transactionInputs: state => state.transaction_input.transaction_inputs
            }),
        },

        methods: {
            async removeAll() {
                this.buttonDisabled = true;
                if (this.transactionInputs.length > 0) {
                    try {

                        await this.$store.dispatch("transaction_input/delete_all");
                        await this.$store.dispatch("seller_firm/get_by_public_id", this.$route.params.public_id);
                        this.$router.push(`/tax/clients/${this.$route.params.public_id}`)

                    } catch (error) {
                        this.$toast.error(error, { duration: 5000 });
                        this.buttonDisabled = false;
                        return [];
                    }
                }
            },
        },
    }
</script>

<style>
</style>
