<template>
  <div>
    <table-transactions :transactions="transactions" />
    <b-button variant="outline-primary" :disabled="buttonFetchDisabled" block @click="refresh">
      <b-spinner v-if="buttonFetchDisabled" small />
      <b-icon v-else icon="chevron-down" />
      Show More
    </b-button>
  </div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name:'OverviewTransactions',

        async fetch() {
            if (
                this.transactions.length === 0 || this.transactions[0]['tax_record_public_id'] !== this.$route.params.public_id
            ) {

                const { store } = this.$nuxt.context
                const params = {
                    tax_record_public_id: this.$route.params.public_id,
                    page: 1
                }
                await store.dispatch("transaction/get_by_tax_record_public_id", params)
            }
        },

        computed: {
            ...mapState({
                transactions: state => state.transaction.transactions
            }),

            buttonFetchDisabled() {
                return this.$fetchState.pending ? true : false
            },
            currentPage() {
               return Math.trunc(this.transactions.length / 25)
            }
        },

        methods: {
            async refresh() {
                const { store } = this.$nuxt.context
                const params = {
                    tax_record_public_id: this.$route.params.public_id,
                    page: this.currentPage + 1
                }
                await store.dispatch("transaction/get_by_tax_record_public_id", params)
            }
        },
    }
</script>

<style>
</style>
