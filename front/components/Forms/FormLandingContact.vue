<template>
  <div>
    <b-row>
      <b-col>
        <b-form-input v-model="form.email" placeholder="Your Email" />
      </b-col>
      <b-col cols="auto">
        <b-button pill variant="outline-primary" @click="subscribe()">
          Submit
        </b-button>
      </b-col>
    </b-row>
    <small class="text-muted mt-4">
      We sent out updates once a month. You can unsubscribe at any time.
    </small>
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
        await store.dispatch("subscriber/create", this.form)
        this.makeToastSuccess()
      } catch (err) {
        console.log(err.response.data.message)
        this.makeToastError(err.response.data.message)
      }
    },

    makeToastSuccess() {
      this.$bvToast.toast("Happy to connect!", {
        title: "Submission Successful",
        variant: "success",
        autoHideDelay: 10000,
      })
    },
    makeToastError(message) {
      this.$bvToast.toast(message, {
        title: "Submission Failed",
        variant: "danger",
        autoHideDelay: 10000,
      })
    },
  },
}
</script>

<style>
</style>
