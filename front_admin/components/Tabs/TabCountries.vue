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
        { value: true, text: "Countries w Currency Only" },
        { value: false, text: "No Filter" },
      ],
    }
  },

  computed: {
    ...mapState({
      countries: (state) => state.country.countries,
    }),

    countriesSelect() {
      return this.selected ? this.$store.getters["country/getInclCurrencyOnly"] : this.countries
    },
  }
}
</script>

<style>
</style>
