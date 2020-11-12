<template>
  <b-tabs vertical pills>
    <b-tab title="Platforms" active>
      <tab-platforms />
    </b-tab>
    <b-tab title="Channels">
      <tab-channels />
    </b-tab>
    <b-tab title="EU" lazy>
      <tab-eu />
    </b-tab>
    <b-tab title="Countries" lazy>
      <tab-countries />
    </b-tab>
    <b-tab title="Currencies" lazy>
      <tab-currencies />
    </b-tab>
    <b-tab title="Tax Treatments" lazy>
      <tab-tax-treatments />
    </b-tab>
    <b-tab title="Tax Rate Types" lazy>
      <h1>Here gets all Tax Rate Types Data</h1>
    </b-tab>
    <b-tab title="Vat Rates" lazy>
      <h1>Here gets all Tax Rate Types Data</h1>
    </b-tab>
    <b-tab title="Vat Thresholds" lazy>
      <h1>Here gets all Vat Thresholds Data</h1>
    </b-tab>
    <b-tab title="Transaction Type" lazy>
      <h1>Here gets all Transaction Types Data</h1>
    </b-tab>
    <b-tab title="Transaction Type Public" lazy>
      <h1>Here gets all Public Transaction Types Data</h1>
    </b-tab>
  </b-tabs>
</template>

<script>
export default {
  name: 'TabsBaseData'

}
</script>

<style>

</style>
