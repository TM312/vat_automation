<template>
  <div>
    <h1 class="mb-5">
      Here is all Currency Data
    </h1>
    <b-row cols="1" cols-lg="2" cols-xl="3">
      <b-col v-for="currency in currencies" :key="currency.code" class="my-2 px-2">
        <card-currency :currency="currency" />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "TabCurrencies",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.currencies.length === 0) {
      await store.dispatch("currency/get_all")
    }
  },

  computed: {
    ...mapState({
      currencies: (state) => state.currency.currencies,
    }),
  },
}
</script>

<style>
</style>
