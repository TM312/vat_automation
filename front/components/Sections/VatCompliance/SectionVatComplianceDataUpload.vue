<template>
  <section id="vat-compliance-data-upload">
    <b-container>
      <div class="text-right">
        <h6 class="text-primary">
          Data Management
        </h6>
        <h2>Simple Set Up &amp; Data Upload</h2>
      </div>
      <p class="lead text-dark mt-3">
        Set up your company account within minutes by filling out the
        provided templates. Your company information is processed on the fly while you receive live status updates.
      </p>
    </b-container>

    <b-row class="my-4">
      <b-col class="mb-4" cols="12" xl="5">
        <b-pagination
          v-model="currentPage"
          class="mb-2"
          :per-page="perPage"
          :total-rows="total"
          pills
          size="md"
          hide-goto-end-buttons
        />
        <div class="product-container mt-3">
          <card-sample
            v-show="currentPage === 1"
            :page="currentPage"
            :total="total"
            primer="Bond Store Ltd"
            description="The sample company at hand is the 'Bond Store Ltd' based in London, GB, providing equipment for special missions as an Amazon seller in the PAN-EU program."
            illustration="seller.svg"
          />
          <card-sample
            v-show="currentPage === 2"
            :page="currentPage"
            :total="total"
            primer="Base Data"
            description="The accurate processing of Amazon's 'Sales Transaction Reports' requires information about a company's items, VAT numbers, existing distance selling acitvations, and Amazon account IDs."
            illustration="processing.svg"
          />
          <card-sample
            v-show="currentPage === 3"
            :page="currentPage"
            :total="total"
            primer="Templates"
            description="Our templates provide an easy way to quickly provide this information within a couple of minutes."
            illustration="data_upload.svg"
          />
        </div>
      </b-col>
      <b-col class="mb-4" cols="12" xl="7">
        <card-data-upload-showcase />
      </b-col>
    </b-row>
  </section>
</template>

<script>
export default {
  name: "SectionVatComplianceDataUpload",

  data() {
    return {
      currentPage: 1,
      perPage: 1,
      total: 3,
    }
  },
  //   props: {
  //     sellerFirm: {
  //       type: Array,
  //       required: true,
  //     },
  //   },
}
</script>

<style>
</style>
