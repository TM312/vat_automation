<template>
  <b-table :items="itemsLocalSales" :fields="fieldsNetVatGross" hover />
</template>

<script>
export default {
  name: "TableLocalSales",

  props: {
    fieldsNetVatGross: {
      type: Array,
      required: true,
    },

    taxRecord: {
      type: Object,
      required: true
    }
  },

  computed: {
    itemsLocalSales() {
      return [
        {
          itemName: "Sales",
          net: this.taxRecord.local_sales_sales_net,
          vat: this.taxRecord.local_sales_sales_vat,
          gross: this.taxRecord.local_sales_sales_gross,
        },
        {
          itemName: "Refunds",
          net: this.taxRecord.local_sales_refunds_net,
          vat: this.taxRecord.local_sales_refunds_vat,
          gross: this.taxRecord.local_sales_refunds_gross,
        },
        {
          itemName: "Total",
          net: this.taxRecord.local_sales_total_net,
          vat: this.taxRecord.local_sales_total_vat,
          gross: this.taxRecord.local_sales_total_gross,
        },
      ]
    },
  }
}
</script>
