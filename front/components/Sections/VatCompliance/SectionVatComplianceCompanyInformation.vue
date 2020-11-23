<template>
  <section id="vat-compliance-company-information">
    <b-tabs pills>
      <b-tab title="Accounts" class="py-3">
        <card-accounts v-if="showcase_accounts" showcase class="neuphormism" />
        <div v-else class="p-5 text-center neuphormism" style="border-rounded: 10px">
          <h6 class="text-muted">
            No data submitted yet. Click on 'Upload' to set up the company account.
          </h6>
        </div>
      </b-tab>
      <b-tab title="VAT Numbers" class="py-3">
        <card-vat-numbers v-if="showcase_distance_sales" showcase class="neuphormism" />
        <div v-else class="p-5 text-center neuphormism" style="border-rounded: 10px">
          <h6 class="text-muted">
            No data submitted yet. Click on 'Upload' to set up the company account.
          </h6>
        </div>
      </b-tab>
      <b-tab title="Distance Sales" class="py-3">
        <card-distance-sales v-if="showcase_vat_numbers" showcase class="neuphormism" />
        <div v-else class="p-5 text-center neuphormism" style="border-rounded: 10px">
          <h6 class="text-muted">
            No data submitted yet. Click on 'Upload' to set up the company account.
          </h6>
        </div>
      </b-tab>
      <b-tab title="Items" class="py-3">
        <card-items v-if="showcase_items" showcase :per-page="5" class="neuphormism" />
        <div v-else class="p-5 text-center neuphormism" style="border-rounded: 10px">
          <h6 class="text-muted">
            No data submitted yet. Click on 'Upload' to set up the company account.
          </h6>
        </div>
      </b-tab>
    </b-tabs>
  </section>
</template>

<script>

import { mapState } from 'vuex'

export default {
  name: "SectionVatComplianceCompanyInformation",
  computed: {
    ...mapState({
      showcase_accounts: state => state.showcase.showcase_accounts,
      showcase_distance_sales: state => state.showcase.showcase_distance_sales,
      showcase_vat_numbers: state => state.showcase.showcase_vat_numbers,
      showcase_items: state => state.showcase.showcase_items,
    })

  },

}
</script>

<style scoped>
.neuphormism {
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }
</style>
