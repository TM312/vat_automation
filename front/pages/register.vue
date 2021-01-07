<template>
  <b-container class="py-5 mb-4">
    <section-register-top class="mb-5" />
    <section-create-form class="mb-5" />
  </b-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  layout: "default",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.countries.length === 0) {
      const y = await store.dispatch("country/get_all")
      console.log(y)
    }
  },

  computed: {
    ...mapState({
      countries: state => state.country.countries
    })
  }
}
</script>

<style>

</style>
