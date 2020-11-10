<template>
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
      <span>{{ country.code }}</span>
      <span v-if="country.vat_country_code">
        | Vat Code: {{ country.vat_country_code }}</span>
    </b-card-sub-title>
    <b-card-text v-if="!!country.currency_code" class="mt-3">
      Currency: {{ country.currency_code }} -
      {{
        $store.getters["currency/getNameByCode"](country.currency_code)
      }}
    </b-card-text>
    <b-card-text class="mt-3">
      Validity: {{ country.valid_from }} -
      {{ country.valid_to }}
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  name: "CardCountry",

  props: {
    country: {
      type: Object,
      required: true,
    }
  },

  data() {
    return {
      edit: false,
      form: {
        name: null
      }
    }
  },
}
</script>

<style>
</style>
