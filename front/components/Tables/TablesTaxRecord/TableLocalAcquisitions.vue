<template>
  <b-table
    :items="itemsLocalAcquisitions"
    :fields="fieldsNetVatGross"
    hover
  />
</template>

<script>
export default {
  name: "TableLocalAcquisitions",

  props: {
    fieldsNetVatGross: {
      type: Array,
      required: true,
    },

    taxRecord: {
      type: Object,
      required: true,
    },
  },

  computed: {
    itemsLocalAcquisitions() {
      return [
        {
          itemName: "Acquisitions",
          net: this.taxRecord.local_acquisitions_acquisitions_net,
          vat: this.taxRecord.local_acquisitions_acquisitions_vat,
          gross: this.taxRecord.local_acquisitions_acquisitions_gross,
        },
        {
          itemName: "Refunds",
          net: this.taxRecord.local_acquisitions_refunds_net,
          vat: this.taxRecord.local_acquisitions_refunds_vat,
          gross: this.taxRecord.local_acquisitions_refunds_gross,
        },
        {
          itemName: "Total",
          net: this.taxRecord.local_acquisitions_total_net,
          vat: this.taxRecord.local_acquisitions_total_vat,
          gross: this.taxRecord.local_acquisitions_total_gross,
        },
      ]
    },
  },


}
</script>
