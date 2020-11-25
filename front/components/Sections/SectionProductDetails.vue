<template>
  <section>
    <h6 class="text-primary">
      Fully Automated Infrastructure
    </h6>
    <h1>File Your Preliminary VAT Tax Returns In Minutes</h1>
    <b-row class="mt-3">
      <b-col cols="12" lg="6">
        <p class="lead text-secondary">
          We are on a mission to provide you with the best experience
          to stay vat compliant and manage your operations.
        </p>
        <b-row>
          <b-col cols="6">
            <p>
              <span><b-icon icon="check-circle" variant="success" /></span>
              <span class="ml-1">VAT Threshold Monitoring</span>
            </p>
            <p>
              <span><b-icon icon="check-circle" variant="success" /></span>
              <span class="ml-1">Easy Data Upload</span>
            </p>
          </b-col>
          <b-col cols="6">
            <p>
              <span><b-icon icon="check-circle" variant="success" /></span>
              <span class="ml-1">Vat Number Validation</span>
            </p>
            <p>
              <span><b-icon icon="check-circle" variant="success" /></span>
              <span class="ml-1">Daily Exchange Rates</span>
            </p>
          </b-col>
          <b-col cols="12">
            <p>
              <span><b-icon icon="check-circle" variant="success" /></span>
              <span class="ml-1">Monitoring Of Reported Amazon Data</span>
            </p>
          </b-col>
        </b-row>

        <button-enter-arrow-right
          to="/vat-compliance"
          content="Product Details"
          class="mt-4"
        />
      </b-col>
      <b-col cols="12" lg="6">
        <!-- <b-embed type="video" aspect="4by3">
            <source
              src="@/assets/vid/Untitled.m4v"
              type="video/mp4"
            />
          </b-embed> -->
        <b-img class="neuphormism" style="border-radius: 10px" fluid src="@/assets/img/product/transaction_inputs_browser.png" />
      </b-col>
    </b-row>
    <div></div>
  </section>
</template>

<script>
export default {
  name: "SectionProductDetails",
}
</script>

<style>
    .neuphormism {
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }
</style>
