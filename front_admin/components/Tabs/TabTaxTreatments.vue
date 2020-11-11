<template>
  <div>
    <h1 class="mb-5">
      Here is all Tax Treatment Data
    </h1>
    <b-row cols="1" cols-lg="2" cols-xl="3">
      <b-col v-for="taxTreatment in taxTreatments" :key="taxTreatment.code" class="my-2 px-2">
        <card-tax-treatment :tax-treatment="taxTreatment" />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "TabTaxTreatments",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.taxTreatments.length === 0) {
      await store.dispatch("tax_treatment/get_all")
    }
  },
  computed: {
    ...mapState({
      taxTreatments: (state) => state.tax_treatment.tax_treatments,
    }),
  },
}
</script>

<style>
</style>
