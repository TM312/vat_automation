<template>
  <div>
    <navbar-tax />
    <b-container fluid>
      <h3 class="text-muted text-center my-3">
        {{ sellerFirm.name }}
      </h3>
      <b-row>
        <b-col cols="auto">
          <navbar-tax-side :client-public-id="sellerFirm.public_id" />
        </b-col>
        <b-col>
          <nuxt />
        </b-col>
      </b-row>
      <!-- <h1>THIS IS THE TAX LAYOUT</h1> -->
    </b-container>
    <Footer />
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  middleware: "auth",

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
    }),
  },
}
</script>
