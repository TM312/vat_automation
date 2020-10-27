<template>
  <div>
    <div v-if="taxRecordOverview">
      <b-tabs content-class="mt-3">
        <b-tab title="Overview" active>
          <div v-if="$fetchState.pending">
            <b-row class="mb-3" cols="1" cols-md="2" cols-xl="4">
              <b-col v-for="i in 20" :key="i" class="mb-2">
                <card-tax-record-short-skeleton />
              </b-col>
            </b-row>
          </div>
          <div v-else>
            <div v-if="taxRecords.length === 0">
              <b-card>
                <b-card-text>
                  <h5 class="text-muted text-center m-5">
                    No Tax Records Created Yet
                  </h5>
                </b-card-text>
              </b-card>
            </div>
            <div v-else>
              <b-row
                class="mb-3"
                cols="1"
                cols-md="2"
                cols-xl="4"
              >
                <b-col
                  v-for="(taxRecord, i) in taxRecords"
                  :key="i"
                  class="mb-2"
                >
                  <card-tax-record-short
                    :tax-record="taxRecord"
                    @single-view="getSingleView($event)"
                  />
                </b-col>
              </b-row>
            </div>
          </div>
        </b-tab>
        <b-tab title="Create New">
          <lazy-form-add-seller-firm-tax-record />
        </b-tab>
      </b-tabs>
    </div>
    <div v-else>
      <lazy-container-tax-record
        :tax-record-public-id="taxRecordPublicId"
        @overview="getOverview"
      />
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "OverviewTaxRecords",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.taxRecords.length == 0) {
      await store.dispatch(
        "tax_record/get_all_by_seller_firm_public_id",
        this.sellerFirm.public_id
      )
    }
  },

  data() {
    return {
      taxRecordPublicId: "",
      taxRecordOverview: true,
    }
  },

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
      taxRecords: (state) => state.tax_record.tax_records,
    }),
  },

  methods: {
    getSingleView(payload) {
      this.taxRecordPublicId = payload
      this.taxRecordOverview = false
    },

    getOverview() {
      this.taxRecordPublicId = ""
      this.taxRecordOverview = true
    },
  },
}
</script>

<style>
</style>
