<template>
  <div>
    <b-card
      v-if="countClients === 0"
      sub-title="A List of Your Customers Will Appear Here Once You Start Uploading Data"
      class="text-center py-5"
    />
    <b-tabs v-else content-class="mt-3">
      <b-tab title="Card View" active>
        <b-row class="mb-3" cols="1" cols-md="2" cols-lg="3" cols-xl="3">
          <b-col v-for="(client, i) in clients" :key="i" class="mb-2">
            <card-client-short :business="client" />
          </b-col>
        </b-row>
      </b-tab>
      <b-tab title="Table View">
        <table-clients-tax :clients="clients" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
    import { mapState } from "vuex"

    export default {
        name: 'ViewClients',

        computed: {
            ...mapState({
                clients: state => state.accounting_firm.accounting_firm.clients,
            }),
            countClients() {
                return this.$store.getters['accounting_firm/countClients']
            },
        },
    }
</script>

<style>
</style>
