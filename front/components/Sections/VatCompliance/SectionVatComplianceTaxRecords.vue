<template>
  <section id="vat-compliance-tax-record-information" class="py-5">
    <div class="text-right">
      <h6 class="text-primary">
        Tax Record Creation
      </h6>
      <h2>Automation At Your Hands</h2>
      <p class="lead text-dark my-2">
        Always have all your tax records in one place. Creating a new
        one, when deadlines are approaching is a piece of cake. Try it
        yourself.
      </p>
    </div>
    <b-tabs v-model="tab" content-class="mt-3">
      <b-tab title="Create New" @click="tab = 0">
        <b-row>
          <b-col cols="12" xl="7">
            <form-add-seller-firm-tax-record
              showcase
              @created="tab = 1"
            />
          </b-col>
          <b-col cols="12" xl="5">
            <div>
              <b-pagination
                v-model="currentPage"
                class="mb-3"
                :per-page="perPage"
                :total-rows="total"
                pills
                size="sm"
                hide-goto-end-buttons
              />
              <card-sample
                v-show="currentPage === 1"
                :page="currentPage"
                :total="total"
                primer="Tax Record Creation"
                description="Create tax records for any country in the PAN-EU program by using the form on the left side."
                illustration="data.svg"
              />
              <card-sample
                v-show="currentPage === 2"
                :page="currentPage"
                :total="total"
                primer="Bond Store Ltd"
                description="For this example, only the 'Sales Tax Transaction Report' for January 2020 was uploaded. Therefore, meaningful tax records would lay between January 1st to January 31st, 2020."
                illustration="data.svg"
              />
            </div>
          </b-col>
        </b-row>
      </b-tab>
      <b-tab title="Overview" @click="tab = 1">
        <view-tax-records
          v-if="Object.keys(sellerFirm).length !== 0"
          :seller-firm="sellerFirm"
          :tax-records="taxRecords"
          showcase
        />
      </b-tab>
    </b-tabs>
    <b-collapse id="collapse-tax-record-tables" class="py-3 mt-2">
      <b-card id="neuphormism">
        <b-card-title>
          <b-row>
            <b-col cols="auto" class="ml-auto">
              <b-button
                size="sm"
                variant="outline-danger"
                @click="
                  $root.$emit(
                    'bv::toggle::collapse',
                    'collapse-tax-record-tables'
                  )
                "
              >
                <b-icon icon="x" />
              </b-button>
            </b-col>
          </b-row>
        </b-card-title>
        <b-card-text>
          <b-tabs pills vertical>
            <b-tab title="Local Sales" active>
              <table-local-sales
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-vat-gross="fieldsNetVatGross"
                :tax-record="taxRecord"
              />
              <small
                v-if="taxTreatments.length !== 0"
                class="mt-2 text-muted"
              >
                {{
                  $store.getters["tax_treatment/getByCode"](
                    "LOCAL_SALE"
                  ).description
                }}
              </small>
            </b-tab>
            <b-tab title="Local Sale Reverse Charges">
              <table-local-sale-reverse-charges
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-vat-gross="fieldsNetVatGross"
                :tax-record="taxRecord"
              />
              <small
                v-if="taxTreatments.length !== 0"
                class="mt-2 text-muted"
              >
                {{
                  $store.getters["tax_treatment/getByCode"](
                    "LOCAL_SALE_REVERSE_CHARGE"
                  ).description
                }}
              </small>
            </b-tab>
            <b-tab title="Distance Sales">
              <table-distance-sales
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-vat-gross="fieldsNetVatGross"
                :tax-record="taxRecord"
              />
              <small
                v-if="taxTreatments.length !== 0"
                class="mt-2 text-muted"
              >
                {{
                  $store.getters["tax_treatment/getByCode"](
                    "DISTANCE_SALE"
                  ).description
                }}
              </small>
            </b-tab>
            <b-tab title="Non-Taxable Distance Sales">
              <table-non-taxable-distance-sales
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-vat-gross="fieldsNetVatGross"
                :tax-record="taxRecord"
              />
              <small
                v-if="taxTreatments.length !== 0"
                class="mt-2 text-muted"
              >
                {{
                  $store.getters["tax_treatment/getByCode"](
                    "NON_TAXABLE_DISTANCE_SALE"
                  ).description
                }}
              </small>
            </b-tab>
            <b-tab title="Intra-Community Sales">
              <table-intra-community-sales
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net="fieldsNet"
                :tax-record="taxRecord"
              />
            </b-tab>
            <b-tab title="Exports">
              <table-exports
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net="fieldsNet"
                :tax-record="taxRecord"
              />
              <small
                v-if="taxTreatments.length !== 0"
                class="mt-2 text-muted"
              >
                {{
                  $store.getters["tax_treatment/getByCode"](
                    "EXPORT"
                  ).description
                }}
              </small>
            </b-tab>
            <b-tab title="Intra-Community Acquisitions">
              <table-intra-community-acquisitions
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-reverse-charge="
                  fieldsNetReverseCharge
                "
                :tax-record="taxRecord"
              />
              <small
                v-if="taxTreatments.length !== 0"
                class="mt-2 text-muted"
              >
                {{
                  $store.getters["tax_treatment/getByCode"](
                    "INTRA_COMMUNITY_ACQUISITION"
                  ).description
                }}
              </small>
            </b-tab>
            <b-tab title="Local Acquisitions">
              <table-local-acquisitions
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-vat-gross="fieldsNetVatGross"
                :tax-record="taxRecord"
              />
              <small
                v-if="taxTreatments.length !== 0"
                class="mt-2 text-muted"
              >
                {{
                  $store.getters["tax_treatment/getByCode"](
                    "LOCAL_ACQUISITION"
                  ).description
                }}
              </small>
            </b-tab>
          </b-tabs>
        </b-card-text>
      </b-card>
    </b-collapse>
  </section>
</template>

<script>
import { mapState } from "vuex"
export default {
  name: "SectionVatComplianceTaxRecords",

  data() {
    return {
      tab: 0,
      taxRecordPublicId: "",
      currentPage: 1,
      perPage: 1,
      total: 2,
    }
  },

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
      taxRecords: (state) => state.tax_record.tax_records,
      taxRecord: (state) => state.tax_record.tax_record,
      taxTreatments: (state) => state.tax_treatment.tax_treatments,
    }),

    taxRecordCurrencyCode() {
      return this.taxRecord ? this.taxRecord.currency_code : ""
    },

    fieldsNet() {
      return [
        {
          key: "itemName",
          label: "",
          sortable: false,
        },
        {
          key: "net",
          sortable: false,
          formatter: (value) => {
            return `${Number.parseFloat(value).toFixed(2)} ${
              this.taxRecordCurrencyCode === "EUR"
                ? "€"
                : this.taxRecordCurrencyCode
            }`
          },
        },
      ]
    },

    fieldsNetReverseCharge() {
      return [
        {
          key: "itemName",
          label: "",
          sortable: false,
        },
        {
          key: "net",
          sortable: false,
          formatter: (value) => {
            return `${Number.parseFloat(value).toFixed(2)} ${
              this.taxRecordCurrencyCode === "EUR"
                ? "€"
                : this.taxRecordCurrencyCode
            }`
          },
        },
        {
          key: "reverseChargeVat",
          sortable: false,
          formatter: (value) => {
            return `${Number.parseFloat(value).toFixed(2)} ${
              this.taxRecordCurrencyCode === "EUR"
                ? "€"
                : this.taxRecordCurrencyCode
            }`
          },
        },
      ]
    },

    fieldsNetVatGross() {
      return [
        {
          key: "itemName",
          label: "",
          sortable: false,
        },
        {
          key: "net",
          sortable: false,
          formatter: (value) => {
            return `${Number.parseFloat(value).toFixed(2)} ${
              this.taxRecordCurrencyCode === "EUR"
                ? "€"
                : this.taxRecordCurrencyCode
            }`
          },
        },
        {
          key: "vat",
          sortable: false,
          formatter: (value) => {
            return `${Number.parseFloat(value).toFixed(2)} ${
              this.taxRecordCurrencyCode === "EUR"
                ? "€"
                : this.taxRecordCurrencyCode
            }`
          },
        },
        {
          key: "gross",
          sortable: false,
          formatter: (value) => {
            return `${Number.parseFloat(value).toFixed(2)} ${
              this.taxRecordCurrencyCode === "EUR"
                ? "€"
                : this.taxRecordCurrencyCode
            }`
          },
        },
      ]
    },
  },
}
</script>

<style scoped>
    #neuphormism {
        border-radius: 5px;
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }
</style>
