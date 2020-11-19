<template>
  <section id="vat-compliance-tax-record-information" class="py-5">
    <div class="text-right">
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
    <b-collapse id="collapse-tax-record-tables" class="py-3 mt-2">
      <b-card id="neuphormism">
        <b-card-title>
          <b-row>
            <b-col cols="auto" class="ml-auto">
              <b-button size="sm" variant="outline-danger" @click="$root.$emit('bv::toggle::collapse', 'collapse-tax-record-tables')">
                <b-icon icon="x" />
              </b-button>
            </b-col>
          </b-row>
        </b-card-title>
        <b-card-text>
          <b-tabs pills vertical>
            <b-tab title="Local Sales" active class="py-3">
              <table-local-sales
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-vat-gross="fieldsNetVatGross"
                :tax-record="taxRecord"
              />
              <p class="text-dark">
                Lorem ipsum dolor sit amet, consetetur sadipscing
                elitr, sed diam nonumy eirmod tempor invidunt ut
                labore et dolore magna aliquyam erat, sed diam
                voluptua. At vero eos et accusam et justo duo
                dolores et ea rebum.
              </p>
            </b-tab>
            <b-tab title="Local Sale Reverse Charges" class="py-3">
              <table-local-sale-reverse-charges
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-vat-gross="fieldsNetVatGross"
                :tax-record="taxRecord"
              />
              <p class="text-dark">
                Lorem ipsum dolor sit amet, consetetur sadipscing
                elitr, sed diam nonumy eirmod tempor invidunt ut
                labore et dolore magna aliquyam erat, sed diam
                voluptua. At vero eos et accusam et justo duo
                dolores et ea rebum.
              </p>
            </b-tab>
            <b-tab title="Distance Sales" class="py-3">
              <table-distance-sales
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-vat-gross="fieldsNetVatGross"
                :tax-record="taxRecord"
              />
              <p class="text-dark">
                Lorem ipsum dolor sit amet, consetetur sadipscing
                elitr, sed diam nonumy eirmod tempor invidunt ut
                labore et dolore magna aliquyam erat, sed diam
                voluptua. At vero eos et accusam et justo duo
                dolores et ea rebum.
              </p>
            </b-tab>
            <b-tab title="Non-Taxable Distance Sales" class="py-3">
              <table-non-taxable-distance-sales
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-vat-gross="fieldsNetVatGross"
                :tax-record="taxRecord"
              />
              <p class="text-dark">
                Lorem ipsum dolor sit amet, consetetur sadipscing
                elitr, sed diam nonumy eirmod tempor invidunt ut
                labore et dolore magna aliquyam erat, sed diam
                voluptua. At vero eos et accusam et justo duo
                dolores et ea rebum.
              </p>
            </b-tab>
            <b-tab title="Intra-Community Sales" class="py-3">
              <table-intra-community-sales
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net="fieldsNet"
                :tax-record="taxRecord"
              />
              <p class="text-dark">
                Lorem ipsum dolor sit amet, consetetur sadipscing
                elitr, sed diam nonumy eirmod tempor invidunt ut
                labore et dolore magna aliquyam erat, sed diam
                voluptua. At vero eos et accusam et justo duo
                dolores et ea rebum.
              </p>
            </b-tab>
            <b-tab title="Exports" class="py-3">
              <table-exports
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net="fieldsNet"
                :tax-record="taxRecord"
              />
              <p class="text-dark">
                Lorem ipsum dolor sit amet, consetetur sadipscing
                elitr, sed diam nonumy eirmod tempor invidunt ut
                labore et dolore magna aliquyam erat, sed diam
                voluptua. At vero eos et accusam et justo duo
                dolores et ea rebum.
              </p>
            </b-tab>
            <b-tab title="Intra-Community Acquisitions" class="py-3">
              <table-intra-community-acquisitions
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-reverse-charge="fieldsNetReverseCharge"
                :tax-record="taxRecord"
              />
              <p class="text-dark">
                Lorem ipsum dolor sit amet, consetetur sadipscing
                elitr, sed diam nonumy eirmod tempor invidunt ut
                labore et dolore magna aliquyam erat, sed diam
                voluptua. At vero eos et accusam et justo duo
                dolores et ea rebum.
              </p>
            </b-tab>
            <b-tab title="Local Acquisitions" class="py-3">
              <table-local-acquisitions
                v-if="Object.keys(taxRecord).length !== 0"
                :fields-net-vat-gross="fieldsNetVatGross"
                :tax-record="taxRecord"
              />
              <p class="text-dark">
                Lorem ipsum dolor sit amet, consetetur sadipscing
                elitr, sed diam nonumy eirmod tempor invidunt ut
                labore et dolore magna aliquyam erat, sed diam
                voluptua. At vero eos et accusam et justo duo
                dolores et ea rebum.
              </p>
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
      taxRecordPublicId: "",
    }
  },

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
      taxRecords: (state) => state.tax_record.tax_records,
      taxRecord: (state) => state.tax_record.tax_record,
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
              this.taxRecordCurrencyCode
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
              this.taxRecordCurrencyCode
            }`
          },
        },
        {
          key: "reverseChargeVat",
          sortable: false,
          formatter: (value) => {
            return `${Number.parseFloat(value).toFixed(2)} ${
              this.taxRecordCurrencyCode
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
              this.taxRecordCurrencyCode
            }`
          },
        },
        {
          key: "vat",
          sortable: false,
          formatter: (value) => {
            return `${Number.parseFloat(value).toFixed(2)} ${
              this.taxRecord.currency_code
            }`
          },
        },
        {
          key: "gross",
          sortable: false,
          formatter: (value) => {
            return `${Number.parseFloat(value).toFixed(2)} ${
              this.taxRecord.currency_code
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
