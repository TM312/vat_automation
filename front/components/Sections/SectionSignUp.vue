<template>
  <section class="my-5">
    <h6 class="text-primary">
      Get In Touch
    </h6>
    <h1>Coming in January 2021</h1>
    <p class="lead my-2">
      Continuous feedback is the best way to build a product you love. Let's start a dialogue.
    </p>
    <b-row cols="1" cols-lg="2" align-v="stretch" class="mt-5">
      <b-col cols="6" lg="5" class="px-5">
        <spaceship-beam />
      </b-col>
      <b-col cols="auto">
        <b-tabs pills class="mt-3">
          <b-tab title="For Amazon Sellers" active>
            <div class="mt-3">
              <p class="lead text-muted">
                If you want to be among the first to learn about and experiment with new features, enter your email below.
                We will use your email for updates about new features and gathering feedback only.
              </p>
              <form-landing-contact class="mt-2" />
            </div>
          </b-tab>
          <b-tab title="For Potential Partners">
            <div class="mt-3">
              <p class="lead text-muted">
                If you are a tax consultant or service provider for
                e-commerce sellers and interested in a collaboration?
                Get in touch! We would love to hear from you.
              </p>
              <br />
              <code style="color:purple">
                contact@tax-automation.com
              </code>
            </div>
          </b-tab>
        </b-tabs>
      </b-col>
    </b-row>
  </section>
</template>

<script>
export default {
  name: "SectionSignUp",
}
</script>
