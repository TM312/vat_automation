<template>
  <b-container fluid class="mt-4">
    <b-tabs pills active-nav-item-class="text-white">
      <b-tab
        v-for="transaction in transactions"
        :key="transaction.tax_treatment_code"
        :title="capitalize(transaction.tax_treatment_code)"
      >
        <lazy-card-transaction
          :transaction="transaction"
          class="pt-4"
        />
      </b-tab>
    </b-tabs>
    <!-- </b-card> -->
  </b-container>
</template>

<script>

export default {
  name: "ViewTransactions",

  props: {
    transactions: {
      type: [Array, Object],
      required: true
    }
  },

}
</script>

<style>
</style>
