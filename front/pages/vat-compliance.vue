<template>
  <div>
    <b-container class="py-5">
      <b-jumbotron bg-variant="transparent" text-variant="dark" header="Building with Sellers' in Mind">
        <template #lead class="text-secondary mt-5">
          Tax-Automation is a technology company that that builds economic infrastructure for the internet.
          Businesses of every size—from new startups to public
          companies—use our software to accept payments and manage their businesses online.

          We believe sustainable, organic growth is the best way to build a lasting company.

          <hr />

          Hi! I'm Derrick Reimer, the founder of SavvyCal.
          Our mission is to cut the friction and awkwardness out of scheduling time with people.

          We’re an indie SaaS company with a little bit of financial backing from TinySeed.
          We believe sustainable, organic growth is the best way to build a lasting company.

          Previously, I was the co-founder of Drip. I host a weekly podcast called The Art of Product.
        </template>
      </b-jumbotron>
    </b-container>

    <b-container>
      <section id="data-upload" class="py-5">
        <b-row>
          <b-col cols="6" lg="4">
            <b-img fluid src="@/assets/img/placeholders/product.png" />
          </b-col>
          <b-col cols="6" lg="8">
            <p class="lead text-dark">
              Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
            </p>
          </b-col>
        </b-row>
      </section>

      <section id="company-information" class="py-5">
        <b-row>
          <b-col cols="6" lg="8">
            <p class="lead text-dark">
              Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
            </p>
          </b-col>
          <b-col cols="6" lg="4">
            <b-img fluid src="@/assets/img/placeholders/product.png" />
          </b-col>
        </b-row>
      </section>

      <section id="transactions-overview" class="py-5">
        <b-row>
          <b-col cols="6" lg="4">
            <b-img fluid src="@/assets/img/placeholders/product.png" />
          </b-col>
          <b-col cols="6" lg="8">
            <p class="lead text-dark">
              Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
            </p>
          </b-col>
        </b-row>
      </section>

      <section id="tax-record-information" class="py-5">
        <b-row>
          <b-col cols="6" lg="8">
            <p class="lead text-dark">
              Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
            </p>
          </b-col>
          <b-col cols="6" lg="4">
            <b-img fluid src="@/assets/img/placeholders/product.png" />
          </b-col>
        </b-row>
      </section>

      <section
        id="sign-up"
        style="max-width: 45rem"
        class="my-5"
        background="light"
      >
        <b-container align-h="center">
          <h6 class="text-primary">
            Let's Get In Touch
          </h6>
          <h3>Help us building a product you love.</h3>
          <form-landing-contact class="my-3" feedback-on />
        </b-container>
      </section>
    </b-container>
  </div>
</template>

<script>
import FormLandingContact from '../components/Forms/FormLandingContact.vue'
export default {
  components: { FormLandingContact },
  layout: "default",
}
</script>

<style>
</style>
