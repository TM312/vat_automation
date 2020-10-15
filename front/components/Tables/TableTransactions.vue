<template>
  <div>
    <b-tabs v-if="transactions.length === 0">
      <b-tab
        v-for="taxTreatment in taxTreatments"
        :key="taxTreatment.code"
        :title="taxTreatment.name"
        :disabled="taxTreatments[0].code !== taxTreatment.code"
      >
        <h5 class="text-muted text-center m-5">
          There are no tax related processes of this tax treatment.
        </h5>
      </b-tab>
    </b-tabs>

    <b-tabs v-else active-nav-item-class="text-primary">
      <b-tab
        v-for="(taxTreatment, index) in taxTreatments"
        :key="taxTreatment.code"
        lazy
        :disabled="filteredTransactions[index].length === 0"
      >
        <template v-slot:title>
          <!-- <b-spinner v-show="flash" type="grow" small></b-spinner> -->
          {{ taxTreatment.name }}
        </template>
        <!-- <lazy-card-transaction
                    v-for="transaction in filteredTransactions[index]"
                    :key="transaction.public_id"
                    :transaction="transaction"
                /> -->


        <b-table :fields="fields" :items="filteredTransactions[index]" hover>
          <template v-slot:cell(type_code)="data">
            <nuxt-link :to="`/tax/transactions/${data.item.transaction_input_public_id}`">
              {{ data.value }}
            </nuxt-link>
          </template>


          <template v-slot:head(departure_to_arrival)>
            <b-row no-gutters class="justify-content-md-center">
              <b-col class="text-right">
                Departure
              </b-col>
              <b-col cols="2" class="text-center">
                <b-icon icon="arrow-right" />
              </b-col>
              <b-col class="text-left">
                Arrival
              </b-col>
            </b-row>
          </template>

          <template v-slot:cell(departure_to_arrival)="data">
            <b-row no-gutters class="justify-content-md-center">
              <b-col class="text-right">
                {{ data.item.departure_country }}
              </b-col>
              <b-col v-if="data.item.departure_country || data.item.arrival_country" cols="2" class="text-center">
                <b-icon icon="arrow-right" />
              </b-col>
              <b-col class="text-left">
                {{ data.item.arrival_country }}
              </b-col>
            </b-row>
          </template>
        </b-table>
      </b-tab>
    </b-tabs>
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
            flash: false,

            fields: [
                {
                    key: 'tax_date',
                    sortable: false,
                },
                {
                    key: 'transaction_input_given_id',
                    lable: 'Given ID',
                    sortable: false,
                },
                {
                    key: 'transaction_input_activity_id',
                    lable: 'Activity ID',
                    sortable: false,
                },
                {
                    key: 'type_code',
                    sortable: false,
                },
                {
                    key: 'departure_to_arrival',
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
    },

    // watch: {
    //     transactions: function(oldVal, newVal) { // watch it
    //         if (oldVal.length !== newVal.length && newVal.length !== 25) {
    //             console.log('old:', oldVal, 'new:', newVal)
    //             this.setFlash()
    //         }
    //     }
    // },

    // methods: {
    //     sleep(ms) {
    //         return new Promise(resolve => setTimeout(resolve, ms));
    //     },

    //     async setFlash() {
    //         this.flash = true
    //         await this.sleep(2000)
    //         this.falsh = false
    //     }
    // }

}
</script>

<style>
</style>
