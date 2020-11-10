<template>
  <div>
    <h1 class="mb-5">
      Here is all Country Data
    </h1>
    <b-form-select v-model="selected" :options="options" />
    <b-row cols="1" cols-lg="2" cols-xl="3">
      <b-col
        v-for="country in countriesSelect"
        :key="country.code"
        class="my-2 px-2"
      >
        <card-country :country="country" />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "TabCountries",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.countries.length === 0) {
      await store.dispatch("country/get_all")
    }
  },

  data() {
    return {
      selected: true,
      options: [
        { value: true, text: "Filter On" },
        { value: false, text: "Show All" },
      ],
    }
  },

  computed: {
    ...mapState({
      countries: (state) => state.country.countries,
    }),
    countriesSelect() {
      if (this.selected) {
        return this.$store.getters["country/getInclCurrencyOnly"]
      } else {
        return this.countries
      }
    },
  },
}
</script>

<style>
</style>
