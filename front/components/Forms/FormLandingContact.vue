<template>
  <div>
    <b-form-input
      id="nested-street"
      v-model="email"
      placeholder="Your Email"
    />
    <small class="text-muted mt-2">No spam. You can unsubscribe at any time.</small>
    <b-button
      pill
      variant="outline-primary"
      block
      class="my-4"
      @click="subscribe()"
    >
      Submit
    </b-button>
  </div>
</template>

<script>
export default {
  name: "FormLandingContact",

  data() {
    return {
      email: ''
    }
  },

  methods: {
    subscribe() {
      this.$axios
      this.email

      this.$axios({
        method: 'GET',
        url: this.urlEndpointTemplate,
        responseType: 'blob'
      })

        .then(
          this.$bvToast.toast('Pleased with your interest and happy to connect!', {
            autoHideDelay: 5000,
            variant: 'success'
          })
        )

        .catch(
          this.$bvToast.toast('An error occured. Please try again later or contact one of the admins.', {
            autoHideDelay: 5000,
            variant: 'danger'
          })
        )

    }
  },
}
</script>

<style>
</style>
