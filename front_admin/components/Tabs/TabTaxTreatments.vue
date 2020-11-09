<template>
  <div>
    <h1 class="mb-5">
      Here is all Tax Treatment Data
    </h1>
    <b-row cols="1" cols-lg="2" cols-xl="3">
      <b-col v-for="tax_treatment in tax_treatments" :key="tax_treatment.code" class="my-2 px-2">
        <b-card class="h-100">
          <b-card-title>
            <b-row>
              <b-col cols="auto">
                {{ tax_treatment.name }}
              </b-col>
              <b-col cols="auto ml-auto">
                <b-button variant="outline-warning" size="sm">
                  <b-icon icon="pencil-square" /> Edit
                </b-button>
              </b-col>
            </b-row>
          </b-card-title>
          <b-card-sub-title>Code: {{ tax_treatment.code }}</b-card-sub-title>
          <b-card-text class="mt-3">
            {{ tax_treatment.description }}
          </b-card-text>
        </b-card>
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
    if (this.tax_treatments.length === 0) {
      await store.dispatch("tax_treatment/get_all")
    }
  },
  computed: {
    ...mapState({
      tax_treatments: (state) => state.tax_treatment.tax_treatments,
    }),
  },
}
</script>

<style>
</style>
