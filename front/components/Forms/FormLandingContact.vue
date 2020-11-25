<template>
  <div>
    <b-form-input v-model="form.email" placeholder="Your Email" />
    <b-form-textarea
      v-if="feedbackOn"
      id="feedback"
      v-model="form.feedback"
      placeholder="Is there any feature you need to are hoping for? Tell us, it's not unlikely that we can build it."
      rows="3"
      max-rows="8"
      class="mt-4"
    />
    <small class="text-muted">
      We sent out updates once a month. You can unsubscribe at any time.
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
    async subscribe() {
      const { store } = this.$nuxt.context
      try {
        await store.dispatch( "subscriber/create", this.form )
        this.makeToastSuccess()
      } catch(err) {
        console.log(err.response.data.message)
        this.makeToastError(err.response.data.message)
      }
    },

    makeToastSuccess() {
      this.$bvToast.toast('Happy to connect!',
        {
          title: "Submission Successful",
          variant: "success",
          autoHideDelay: 10000,
        }
      )
    },
    makeToastError(message) {
      this.$bvToast.toast(message, {
        title: "Submission Failed",
        variant: "danger",
        autoHideDelay: 10000,
      })
    }

  }
}
</script>

<style>
</style>
