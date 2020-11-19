<template>
  <b-table
    :items="itemsLocalSaleReverseCharges"
    :fields="fieldsNetVatGross"
    hover
  />
</template>

<script>
export default {
  name: "TableLocalSaleReverseCharges",

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
    itemsLocalSaleReverseCharges() {
      return [
        {
          itemName: "Sales",
          net: this.taxRecord.local_sale_reverse_charges_sales_net,
          vat: this.taxRecord.local_sale_reverse_charges_sales_vat,
          gross: this.taxRecord
            .local_sale_reverse_charges_sales_gross,
        },
        {
          itemName: "Refunds",
          net: this.taxRecord.local_sale_reverse_charges_refunds_net,
          vat: this.taxRecord.local_sale_reverse_charges_refunds_vat,
          gross: this.taxRecord
            .local_sale_reverse_charges_refunds_gross,
        },
        {
          itemName: "Total",
          net: this.taxRecord.local_sale_reverse_charges_total_net,
          vat: this.taxRecord.local_sale_reverse_charges_total_vat,
          gross: this.taxRecord
            .local_sale_reverse_charges_total_gross,
        },
      ]
    }
  }
}
</script>

<style>
</style>
