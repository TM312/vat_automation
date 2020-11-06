<template>
  <div>
    <b-row class="mb-3" cols="1" cols-md="2" cols-lg="4">
      <b-col>
        <b-card
          :title="this.$auth.user.key_accounts.length.toString()"
          :sub-title="(this.$auth.user.key_accounts.length == 1) ? 'Key Account' : 'Key Accounts'"
          border-variant="info"
        />
      </b-col>
      <b-col>
        <!-- <p>cards</p> -->
      </b-col>
      <b-col>
        <!-- <p>another card</p> -->
      </b-col>
      <b-col>
        <!-- <p>another card</p> -->
      </b-col>
    </b-row>
  </div>
</template>

<script>

export default {
  name: 'DashboardDashboard',

}
</script>

<style>

</style>
