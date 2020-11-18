<template>
  <section id="vat-compliance-tax-record-information" class="py-5">
    <div>
      <h6 class="text-primary">
        Step 4
      </h6>
      <h1>Create Tax Records</h1>
      <p class="lead my-2">
        Get unparalleled insights by reviewing the processing of each
        individual transaction.
      </p>
    </div>
    <b-tabs content-class="mt-3">
      <b-tab title="Create New" active>
        <form-add-seller-firm-tax-record showcase />
      </b-tab>
      <b-tab title="Overview">
        <view-tax-records
          :seller-firm="sellerFirm"
          :tax-records="taxRecords"
          showcase
        />
      </b-tab>
    </b-tabs>
  </section>
</template>

<script>
import { mapState } from "vuex"
export default {
  name: "SectionVatComplianceTaxRecords",

  data() {
    return {
      taxRecordPublicId: "",
    }
  },

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
      taxRecords: (state) => state.tax_record.tax_records,
    }),
  },
}
</script>
