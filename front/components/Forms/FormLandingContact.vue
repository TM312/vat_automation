<template>
  <div>
    <b-form-input v-model="form.email" placeholder="Your Email" />
    <b-form-textarea
      v-if="feedbackOn"
      id="feedback"
      v-model="form.feedback"
      placeholder="Is there any feature that would make our service more useful for you? Just let us know here."
      rows="3"
      max-rows="8"
      class="mt-4"
    />
    <small class="text-muted">
      We sent out updates around once a month. You can unsubscribe at any
      time.
    </small>
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

  props: {
    feedbackOn: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      form: {
        email: "",
        feedback: "",
      },
    }
  },

  methods: {
    subscribe() {
      this.$axios
      //   this.form.email
      //   this.form.feedback

      this.$axios({
        method: "GET",
        url: this.urlEndpointTemplate,
        responseType: "blob",
      })

        .then(
          this.$bvToast.toast(
            "Pleased with your interest and happy to connect!",
            {
              autoHideDelay: 5000,
              variant: "success",
            }
          )
        )

        .catch(
          this.$bvToast.toast(
            "An error occured. Please try again later or contact one of the admins.",
            {
              autoHideDelay: 5000,
              variant: "danger",
            }
          )
        )
    },
  },
}
</script>

<style>
</style>
