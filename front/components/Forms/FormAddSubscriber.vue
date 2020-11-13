<template>
  <div>
    <b-form-group>
      <b-form-input id="nested-street" placeholder="Your Email" />
    </b-form-group>
    <b-form-radio-group
      class="pt-2"
      :options="['Amazon Seller', 'Tax Auditor', 'Other']"
    />
    <b-button variant="primary" block>
      <b-icon icon="check-circle" />
      <span>Submit</span>
    </b-button>
  </div>
</template>

<script>
export default {
  name: "FormAddSubscriber"
}
</script>

<style>
</style>
