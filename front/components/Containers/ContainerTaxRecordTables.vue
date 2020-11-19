<template>
  <b-container fluid class="my-3">
    <b-row class="my-5 px-3" cols="1" cols-xl="2">
      <b-col class="mb-2 pr-5">
        <h3>Local Sales</h3>
        <table-local-sales
          :fields-net-vat-gross="fieldsNetVatGross"
          :tax-record="taxRecord"
        />
      </b-col>

      <b-col class="mb-2 pr-5">
        <h3>Local Sale Reverse Charges</h3>
        <table-local-sale-reverse-charges
          :fields-net-vat-gross="fieldsNetVatGross"
          :tax-record="taxRecord"
        />
      </b-col>
    </b-row>

    <b-row class="my-5" cols="1" cols-xl="2">
      <b-col class="mb-2 pr-5">
        <h3>Distance Sales</h3>
        <table-distance-sales
          :fields-net-vat-gross="fieldsNetVatGross"
          :tax-record="taxRecord"
        />
      </b-col>

      <b-col class="mb-2 pr-5">
        <h3>Non-Taxable Distance Sales</h3>
        <table-non-taxable-distance-sales
          :fields-net-vat-gross="fieldsNetVatGross"
          :tax-record="taxRecord"
        />
      </b-col>
    </b-row>

    <b-row class="my-5" cols="1" cols-xl="2">
      <b-col class="mb-2 pr-5">
        <h3>Intra-Community Sales</h3>
        <table-intra-community-sales
          :fields-net="fieldsNet"
          :tax-record="taxRecord"
        />
      </b-col>

      <b-col class="mb-2 pr-5">
        <h3>Exports</h3>
        <table-exports
          :fields-net="fieldsNet"
          :tax-record="taxRecord"
        />
      </b-col>
    </b-row>

    <b-row class="my-5" cols="1" cols-xl="2">
      <b-col class="mb-2 pr-5">
        <h3>Intra-Community Acquisitions</h3>
        <table-intra-community-acquisitions
          :fields-net-reverse-charge="fieldsNetReverseCharge"
          :tax-record="taxRecord"
        />
      </b-col>

      <b-col class="mb-2 pr-5">
        <h3>Local Acquisitions</h3>
        <table-local-acquisitions
          :fields-net-vat-gross="fieldsNetVatGross"
          :tax-record="taxRecord"
        />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "ContainerTaxRecordTables",

  data() {
    return {

      fieldsNet: [
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
              this.taxRecord.currency_code
            }`
          },
        },
      ],

      fieldsNetReverseCharge: [
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
              this.taxRecord.currency_code
            }`
          },
        },
        {
          key: "reverseChargeVat",
          sortable: false,
          formatter: (value) => {
            return `${Number.parseFloat(value).toFixed(2)} ${
              this.taxRecord.currency_code
            }`
          },
        },
      ],

      fieldsNetVatGross: [
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
              this.taxRecord.currency_code
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
      ],
    }
  },

  computed: {
    ...mapState({
      taxRecord: (state) => state.tax_record.tax_record,
    }),


  },

}
</script>

<style>
</style>
