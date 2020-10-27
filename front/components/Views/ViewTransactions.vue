<template>
  <div>
    <b-card
      border-variant="primary"
      header-bg-variant="primary"
      header-text-variant="white"
    >
      <b-tabs pills active-nav-item-class="text-white">
        <b-tab
          v-for="transaction in transactions"
          :key="transaction.tax_treatment_code"
          :title="capitalize(transaction.tax_treatment_code)"
        >
          <lazy-card-transaction
            :transaction="transaction"
            class="mt-4"
          />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
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
