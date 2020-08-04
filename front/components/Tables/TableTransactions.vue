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
                    <!-- <lazy-card-transaction
                        v-for="transaction in filteredTransactions[index]"
                        :key="transaction.public_id"
                        :transaction="transaction"
                    /> -->


                    <b-table :fields="fields" :items="filteredTransactions[index]" hover>

                        <template v-slot:cell(type_code)="data">
                            <nuxt-link :to="`/tax/transactions/${data.item.transaction_input_public_id}`">{{ data.value }}</nuxt-link>
                        </template>


                        <template v-slot:head(departure_to_arrival)>
                            <b-row no-gutters class="justify-content-md-center">
                                <b-col class="text-right">Departure</b-col>
                                <b-col cols="2" class="text-center"><b-icon icon="arrow-right" /></b-col>
                                <b-col class="text-left">Arrival</b-col>
                            </b-row>
                        </template>

                         <template v-slot:cell(departure_to_arrival)="data">
                            <b-row no-gutters class="justify-content-md-center">
                                <b-col class="text-right">{{ data.item.departure_country }}</b-col>
                                <b-col v-if="data.item.departure_country || data.item.arrival_country" cols="2" class="text-center"><b-icon icon="arrow-right" /></b-col>
                                <b-col class="text-left">{{ data.item.arrival_country }}</b-col>
                            </b-row>
                        </template>

                    </b-table>


                </b-tab>
            </b-tabs>

        </b-card>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: "TableTransactions",

    props: {
        transactions: {
            type: [Array, Object],
            required: true
        }
    },

    data() {
        return {
            fields: [
                {
                    key: 'type_code',
                    sortable: false,
                },
                {
                    key: 'departure_to_arrival',
                    sortable: false,
                },
                {
                    key: 'tax_date',
                    sortable: false,
                },
            ],
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
