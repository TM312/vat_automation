<template>
  <div>
    <b-row class="mb-3" cols="1" cols-md="2" cols-lg="4">
      <b-col class="mb-2">
        <card-total-count-function :counter-function="countEmployees" sub-title="Employee Accounts" />
      </b-col>
      <b-col class="mb-2">
        <card-total-count-function :counter-function="countClients" sub-title="Clients" />
      </b-col>
      <b-col class="mb-2">
        <!-- <card-total-count-function :counterFunction="countClients" subTitle="Total Number of Something Else" /> -->
      </b-col>
      <b-col class="mb-2">
        <!-- <card-total-count-function :counterFunction="countClients" subTitle="Total Number of Something Else  4th" /> -->
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: 'ClientsDashboard',

  methods: {
    countClients() {
      return this.$store.getters['accounting_firm/countClients']
    },
    countEmployees() {
      return this.$store.getters['accounting_firm/countEmployees']
    },
  }
}
</script>

<style>

</style>
