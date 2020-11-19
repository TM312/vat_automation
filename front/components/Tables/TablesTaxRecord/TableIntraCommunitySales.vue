<template>
  <b-table :items="itemsIntraCommunitySales" :fields="fieldsNet" hover />
</template>

<script>
export default {
  name: "TableIntraCommunitySales",

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
    itemsIntraCommunitySales() {
      return [
        {
          itemName: "Sales",
          net: this.taxRecord.intra_community_sales_sales_net,
        },
        {
          itemName: "Refunds",
          net: this.taxRecord.intra_community_sales_refunds_net,
        },
        {
          itemName: "Total",
          net: this.taxRecord.intra_community_sales_total_net,
        },
      ]
    },
  },


}
</script>
