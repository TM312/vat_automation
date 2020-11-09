<template>
  <b-container class="my-5">
    <b-tabs content-class="mt-3 py-3">
      <b-tab title="General" active>
        <b>Email:</b>
        {{ user.email }}
        <br />
        <b>Employer:</b>
        {{ user.employer_name }}
        <br />
        <b>Registered On:</b>
        {{ user.registered_on }}
        <br />
      </b-tab>
    </b-tabs>
  </b-container>
</template>

<script>
export default {
  name: "Settings",
  layout: 'admin',
  data() {
    return {
      user: ""
    }
  },

  created() {
    this.user = this.$auth.user
  }
}
</script>

<style></style>
