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
        <b-card class="h-100">
          <b-card-title>
            <b-row>
              <b-col cols="auto">
                {{ country.name }}
              </b-col>
              <b-col cols="auto ml-auto">
                <b-button variant="outline-warning" size="sm">
                  <b-icon icon="pencil-square" /> Edit
                </b-button>
              </b-col>
            </b-row>
          </b-card-title>
          <b-card-sub-title>
            {{ country.code }} | Vat Code:
            {{ country.vat_country_code }}
          </b-card-sub-title>
          <b-card-text v-if="!!country.currency_code" class="mt-3">
            Currency: {{ country.currency_code }} - {{ $store.getters["currency/getNameByCode"](country.currency_code) }}
          </b-card-text>
          <b-card-text class="mt-3">
            Validity: {{ country.valid_from }} -
            {{ country.valid_to }}
          </b-card-text>
        </b-card>
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
