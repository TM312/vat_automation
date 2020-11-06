<template>
  <div>
    <b-tabs pills>
      <b-tab
        v-for="taxTreatment in taxTreatments"
        :key="taxTreatment.code"
        lazy
      >
        <template v-slot:title>
          {{ taxTreatment.name }}s
        </template>

        <table-transactions :tax-treatment-code="taxTreatment.code" class="mt-3" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name:'OverviewTransactions',



  computed: {
    ...mapState({
      taxRecord: (state) => state.tax_record.tax_record,
      taxTreatments: state => state.tax_treatment.tax_treatments,
    }),

  },

}
</script>

<style>
</style>
