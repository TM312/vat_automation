<template>
  <b-table :items="itemsExports" :fields="fieldsNet" hover />
</template>

<script>
export default {
  name: "TableExports",

  props: {
    fieldsNet: {
      type: Array,
      required: true,
    },

    taxRecord: {
      type: Object,
      required: true,
    },
  },

  computed: {
    itemsExports() {
      return [
        {
          itemName: "Sales",
          net: this.taxRecord.exports_sales_net,
        },
        {
          itemName: "Refunds",
          net: this.taxRecord.exports_refunds_net,
        },
        {
          itemName: "Total",
          net: this.taxRecord.exports_total_net,
        },
      ]
    },
  },


}
</script>
