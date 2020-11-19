<template>
  <b-table
    :items="itemsDistanceSales"
    :fields="fieldsNetVatGross"
    hover
  />
</template>

<script>
export default {
  name: "TableDistanceSales",

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
    itemsDistanceSales() {
      return [
        {
          itemName: "Sales",
          net: this.taxRecord.distance_sales_sales_net,
          vat: this.taxRecord.distance_sales_sales_vat,
          gross: this.taxRecord.distance_sales_sales_gross,
        },
        {
          itemName: "Refunds",
          net: this.taxRecord.distance_sales_refunds_net,
          vat: this.taxRecord.distance_sales_refunds_vat,
          gross: this.taxRecord.distance_sales_refunds_gross,
        },
        {
          itemName: "Total",
          net: this.taxRecord.distance_sales_total_net,
          vat: this.taxRecord.distance_sales_total_vat,
          gross: this.taxRecord.distance_sales_total_gross,
        },
      ]
    },
  },

}
</script>
