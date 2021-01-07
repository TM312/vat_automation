<template>
  <section id="vat-compliance-company-information">
    <b-tabs pills>
      <b-tab title="Accounts" class="py-3">
        <card-accounts v-if="showcaseAccounts" showcase class="neuphormism" />
        <div v-else class="p-5 text-center neuphormism" style="border-rounded: 10px">
          <h6 class="text-muted">
            No data submitted yet. Click on 'Upload' to set up the company account.
          </h6>
        </div>
      </b-tab>
      <b-tab title="VAT Numbers" class="py-3">
        <card-vat-numbers v-if="showcaseDistanceSales" showcase class="neuphormism" />
        <div v-else class="p-5 text-center neuphormism" style="border-rounded: 10px">
          <h6 class="text-muted">
            No data submitted yet. Click on 'Upload' to set up the company account.
          </h6>
        </div>
      </b-tab>
      <b-tab title="Distance Sales" class="py-3">
        <card-distance-sales v-if="showcaseVatNumbers" showcase class="neuphormism" />
        <div v-else class="p-5 text-center neuphormism" style="border-rounded: 10px">
          <h6 class="text-muted">
            No data submitted yet. Click on 'Upload' to set up the company account.
          </h6>
        </div>
      </b-tab>
      <b-tab title="Items" class="py-3">
        <card-items v-if="showcaseItems" showcase :per-page="5" class="neuphormism" />
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
      showcaseAccounts: state => state.showcase.showcase_accounts,
      showcaseDistanceSales: state => state.showcase.showcase_distance_sales,
      showcaseVatNumbers: state => state.showcase.showcase_vat_numbers,
      showcaseItems: state => state.showcase.showcase_items,
    })

  },

}
</script>

<style scoped>
.neuphormism {
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }
</style>
