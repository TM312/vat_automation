<template>
    <div>
        <b-card
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

    props: {
        transactions: {
            type: [Array, Object],
            required: true
        }
    },


    computed: {
        ...mapState({
            taxTreatments: state => state.tax_treatment.tax_treatments
        }),

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
