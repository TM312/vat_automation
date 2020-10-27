<template>
  <div>
    <b-tabs active-nav-item-class="text-primary">
      <b-tab
        v-for="taxTreatment in taxTreatments"
        :key="taxTreatment.code"
        lazy
      >
        <template v-slot:title>
          {{ taxTreatment.name }}s
        </template>

        <table-transactions v-once :tax-treatment-code="taxTreatment.code" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name:'OverviewTransactions',

  //   async fetch() {
  //     if (this.transactions.length === 0) {
  //       console.log('this.transactions.length === 0:', this.transactions.length === 0)
  //       const { store } = this.$nuxt.context
  //       const params = {
  //         tax_record_public_id: this.taxRecord.public_id,
  //         page: 1
  //       }
  //       await store.dispatch("transaction/get_by_tax_record", params)
  //     }
  //   },



  computed: {
    ...mapState({
      taxRecord: (state) => state.tax_record.tax_record,
      taxTreatments: state => state.tax_treatment.tax_treatments,
    }),

    // filteredTransactions: function() {
    //     var transactions = this.transactions
    //     return this.taxTreatments.map(function(taxTreatment) {
    //         return transactions.filter(transaction => transaction.tax_treatment_code === taxTreatment.code)
    //     })
    // }
  },

}
</script>

<style>
</style>
