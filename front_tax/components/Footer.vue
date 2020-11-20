<template>
  <footer class="app-footer">
    <b-container class="py-5">
      <b-row>
        <b-col cols="6">
          <span align-self="center" class="text-dark">&copy; Tax-Automation.com</span>
        </b-col>
        <b-col>
          <b-row>
            <b-col>
              <h6>Products</h6><br />
              <nuxt-link to="/vat-compliance">
                Vat Compliance
              </nuxt-link><br />
            </b-col>
            <b-col>
              <h6>Company</h6><br />
              <nuxt-link to="/about">
                About
              </nuxt-link><br />
              <nuxt-link to="/pricing">
                Pricing
              </nuxt-link><br />
              <nuxt-link to="/contact">
                Contact
              </nuxt-link><br />
              <nuxt-link to="/privacy">
                Privacy &amp; Terms
              </nuxt-link>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </footer>
</template>
<script>
export default {
  name: "Footer",
}
</script>
