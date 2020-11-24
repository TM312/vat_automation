<template>
  <section id="vat-compliance-sign-up" style="max-width: 45rem">
    <b-container align-h="center">
      <div v-if="Object.keys(subscriber).length === 0">
        <h6 class="text-primary">
          Let's Get In Touch
        </h6>
        <h3>
          Help us build a product you
          <b-icon icon="heart-fill" variant="danger" />
        </h3>

        <form-landing-contact class="my-3" feedback-on />
      </div>
      <div v-else>
        <h6 class="text-primary">
          Please with your interest
        </h6>
        <h3>
          Help us build a product you
          <b-icon icon="heart-fill" variant="danger" />
        </h3>

        <b-form-input>
          <template #value>
            {{ subscriber.email }} <b-icon icon="check-circle" variant="success" />
          </template>
        </b-form-input>
      </div>
    </b-container>
  </section>
</template>

<script>
import { mapState } from "vuex"
export default {
  name: "SectionSignUpSellers",

  computed: {
    ...mapState({
      subscriber: (state) => state.subscriber.subscriber,
    }),
  },
}
</script>

<style>
</style>
