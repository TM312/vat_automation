<template>
  <b-table
    :items="itemsIntraCommunityAcquisitions"
    :fields="fieldsNetReverseCharge"
    hover
  />
</template>

<script>
export default {
  name: "TableIntraCommunityAcquisitions",

  props: {
    fieldsNetReverseCharge: {
      type: Array,
      required: true,
    },

    taxRecord: {
      type: Object,
      required: true,
    },
  },

  computed: {
    itemsIntraCommunityAcquisitions() {
      return [
        {
          itemName: "Acquisitions",
          net: this.taxRecord.ica_acquisitions_net,
          reverseChargeVat: this.taxRecord
            .ica_acquisitions_reverse_charge_vat,
        },
        {
          itemName: "Refunds",
          net: this.taxRecord.ica_refunds_net,
          reverseChargeVat: this.taxRecord
            .ica_refunds_reverse_charge_vat,
        },
        {
          itemName: "Total",
          net: this.taxRecord.ica_total_net,
          reverseChargeVat: this.taxRecord
            .ica_total_reverse_charge_vat,
        },
      ]
    },
  },


}
</script>
