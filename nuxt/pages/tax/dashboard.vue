<template>
  <b-container fluid>
    <div>Notifications</div>
    <hr>
    <Metrics />
  </b-container>
</template>

<script>
import Metrics from '@/components/TaxAuditor/Dashboard/Metrics'
// import { mapState } from 'vuex'

  export default {
    layout: 'tax',
    components: {
      Metrics
    },
    // async fetch({ store }) {
    //   await store.dispatch('tax_auditor/get_tax_auditor')
    // },
    // computed: {
    //   ...mapState({
    //     tax_auditors: (state) => {
    //       return state.tax_auditor.tax_auditor
    //     }
    //   })
    // }
  }
</script>

<style>
</style>
