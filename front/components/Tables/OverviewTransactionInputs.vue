<template>
    <div>
        <b-button v-if="transactionInputs.length > 0" variant="outline-danger" class="align-right" :disabled="buttonRemoveDisabled" @click="removeAll">Delete All</b-button>
        <b-tabs pills content-class="mt-3">
            <b-tab title="Total" active>
                <b-card
                    v-if="transactionInputs.length === 0"
                    sub-title="An Overview Of Transactions Will Appear Here Once You Start Uploading Data"
                    class="text-center py-5"
                ></b-card>
                <table-transaction-inputs v-else />
                <b-button variant="outline-primary" :disabled="buttonFetchDisabled" @click="refresh" block>
                    <b-spinner v-if="buttonFetchDisabled" small />
                    <b-icon v-else icon="chevron-down" />
                    Show More
                </b-button>

            </b-tab>
            <b-tab v-for="account in sellerFirm.accounts" :key="account.public_id" :title="account.channel_code">
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
                buttonRemoveDisabled: false,
            }
        },

        async fetch() {
            if (
                this.transactionInputs.length === 0 || this.transaction_inputs[0]['seller_firm_public_id'] !== this.$route.params.public_id
            ) {

                const { store } = this.$nuxt.context;
                const params = {
                    seller_firm_public_id: this.$route.params.public_id,
                    page: 1
                }
                await store.dispatch("transaction_input/get_by_seller_firm_public_id", params);
            }
        },

        computed: {
            ...mapState({
                sellerFirm: state => state.seller_firm.seller_firm,
                transactionInputs: state => state.transaction_input.transaction_inputs
            }),

            buttonFetchDisabled() {
                return this.$fetchState.pending ? true : false
            },
            currentPage() {
               return Math.trunc(this.transactionInputs.length / 25)
            }
        },

        methods: {
            async refresh() {
                const { store } = this.$nuxt.context;
                const params = {
                    seller_firm_public_id: this.$route.params.public_id,
                    page: this.currentPage + 1
                }
                await store.dispatch("transaction_input/get_by_seller_firm_public_id", params);
            },

            async removeAll() {
                this.buttonRemoveDisabled = true;
                if (this.transactionInputs.length > 0) {
                    try {

                        await this.$store.dispatch("transaction_input/delete_all");
                        await this.$store.dispatch("seller_firm/get_by_public_id", this.$route.params.public_id);
                        this.$router.push(`/tax/clients/${this.$route.params.public_id}`)

                    } catch (error) {
                        this.$toast.error(error, { duration: 5000 });
                        this.buttonRemoveDisabled = false;
                        return [];
                    }
                }
            },
        },
    }
</script>

<style>
</style>
