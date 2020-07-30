<template>
    <div>
        <b-card
            v-if="!$fetchState.pending"
            no-body
            border-variant="primary"
            header-bg-variant="primary"
            header-text-variant="white"
            >
            <b-tabs v-if="transactions.length === 0" card>
                 <b-tab
                    v-for="taxTreatment in taxTreatments"
                    :key="taxTreatment.code"
                    :title="taxTreatment.name"
                    :disabled="taxTreatments[0].code !== taxTreatment.code"
                ><h5 class="text-muted text-center m-5" > There are no tax related processes for this transaction. </h5>
                </b-tab>
            </b-tabs>

            <b-tabs v-else card active-nav-item-class="text-primary">
                <b-tab
                    v-for="(taxTreatment, index) in taxTreatments"
                    :key="taxTreatment.code"
                    :title="taxTreatment.name"
                    lazy
                    :disabled="filteredTransactions[index].length === 0"
                >
                    <lazy-card-transaction
                        v-for="transaction in filteredTransactions[index]"
                        :key="transaction.public_id"
                        :transaction="transaction"
                    />
                </b-tab>
            </b-tabs>

        </b-card>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: "ViewTransactions",

    async fetch() {
            if (this.taxTreatments.length === 0) {
                const { store } = this.$nuxt.context;
                await store.dispatch("tax_treatment/get_all");
            }
        },


    computed: {
        ...mapState({
            transactions: state => state.transaction_input.transaction_input.transactions,
            taxTreatments: state => state.tax_treatment.tax_treatments
        }),

        // fullNames: function() {
        // return this.items.map(function(item) {
        //     return item.firstname + ' ' + item.lastname;
        // });

        filteredTransactions: function() {
            var transactions = this.transactions
            return this.taxTreatments.map(function(taxTreatment) {
                return transactions.filter(transaction => transaction.tax_treatment_code === taxTreatment.code)
            })
        }
    }
}
</script>

<style>
</style>
