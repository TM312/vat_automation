<template>
  <b-container fluid class="my-3">
    <b-tabs pills vertical>
      <b-tab title="Seller Firms" active>
        <tab-seller-firms />
      </b-tab>
      <b-tab title="Accounts" lazy>
        <tab-accounts />
      </b-tab>
    </b-tabs>
  </b-container>
</template>

<script>
export default {
  layout: 'admin',


}
</script>

<style></style>
