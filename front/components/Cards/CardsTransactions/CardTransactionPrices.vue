<template>
  <b-card title="Prices">
    <div class="mt-3">
      <b-table
        hover
        fixed
        :items="itemsItem"
        :fields="fieldsItemPrices"
        class="mb-4"
      />
    </div>
    <div class="my-3">
      <b-table
        hover
        fixed
        :items="itemsShipment"
        :fields="fieldsShipmentPrices"
        class="mb-4"
      />
    </div>
    <div>
      <b-table
        hover
        fixed
        :items="itemsGiftWrap"
        :fields="fieldsGiftWrapPrices"
        class="mb-4"
      />
    </div>
    <div class="mt-2">
      <b-table
        hover
        fixed
        :items="itemsTotal"
        :fields="fieldsTotalPrices"
        class="mb-4"
      />
    </div>
  </b-card>
</template>

<script>
export default {
  name: "CardTransactionPrices",
  props: {
    transaction: {
      type: [Array, Object],
      required: true,
    }
  },
  computed: {
    itemsItem() {
      return [
        {
          x: "Price",
          net: `${Number.parseFloat(
            this.transaction.item_price_net
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          vat: `${Number.parseFloat(
            this.transaction.item_price_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: `${Number.parseFloat(
            this.transaction.item_price_net +
                                this.transaction.item_price_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
        },
        {
          x: "Discount",
          net: `${Number.parseFloat(
            this.transaction.item_price_discount_net
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          vat: `${Number.parseFloat(
            this.transaction.item_price_discount_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: `${Number.parseFloat(
            this.transaction.item_price_discount_net +
                                this.transaction.item_price_discount_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
        },
        {
          x: "Total",
          net: `${Number.parseFloat(
            this.transaction.item_price_total_net
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          vat: `${Number.parseFloat(
            this.transaction.item_price_total_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: `${Number.parseFloat(
            this.transaction.item_price_total_net +
                                this.transaction.item_price_total_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
        },
      ]
    },

    itemsShipment() {
      return [
        {
          x: "Price",
          net: `${Number.parseFloat(
            this.transaction.shipment_price_net
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          vat: `${Number.parseFloat(
            this.transaction.shipment_price_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: `${Number.parseFloat(
            this.transaction.shipment_price_net +
                                this.transaction.shipment_price_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
        },
        {
          x: "Discount",
          net: `${Number.parseFloat(
            this.transaction.shipment_price_discount_net
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          vat: `${Number.parseFloat(
            this.transaction.shipment_price_discount_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: `${Number.parseFloat(
            this.transaction.shipment_price_discount_net +
                                this.transaction.shipment_price_discount_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
        },
        {
          x: "Total",
          net: `${Number.parseFloat(
            this.transaction.shipment_price_total_net
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          vat: `${Number.parseFloat(
            this.transaction.shipment_price_total_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: `${Number.parseFloat(
            this.transaction.shipment_price_total_net +
                                this.transaction.shipment_price_total_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
        },
      ]
    },

    itemsGiftWrap() {
      return [
        {
          x: "Price",
          net: `${Number.parseFloat(
            this.transaction.gift_wrap_price_net
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          vat: `${Number.parseFloat(
            this.transaction.gift_wrap_price_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: `${Number.parseFloat(
            this.transaction.gift_wrap_price_net +
                                this.transaction.gift_wrap_price_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
        },
        {
          x: "Discount",
          net: `${Number.parseFloat(
            this.transaction.gift_wrap_price_discount_net
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          vat: `${Number.parseFloat(
            this.transaction.gift_wrap_price_discount_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: `${Number.parseFloat(
            this.transaction.gift_wrap_price_discount_net +
                                this.transaction.gift_wrap_price_discount_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
        },
        {
          x: "Total",
          net: `${Number.parseFloat(
            this.transaction.gift_wrap_price_total_net
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          vat: `${Number.parseFloat(
            this.transaction.gift_wrap_price_total_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: `${Number.parseFloat(
            this.transaction.gift_wrap_price_total_net +
                                this.transaction.gift_wrap_price_total_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
        },
      ]
    },

    itemsTotal() {
      return [
        {
          x: "Total",
          net: `${Number.parseFloat(
            this.transaction.total_value_net
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          vat: `${Number.parseFloat(
            this.transaction.total_value_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: `${Number.parseFloat(
            this.transaction.total_value_gross +
                                this.transaction.gift_wrap_price_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
        },
        {
          x: `Reverse Charge (Rate: ${Number.parseFloat(
            this.transaction.reverse_charge_vat_rate * 100
          ).toFixed(2)}%)`,
          net: "-",
          vat: `${Number.parseFloat(
            this.transaction.invoice_amount_reverse_charge_vat
          ).toFixed(2)} ${
            this.transaction.transaction_currency_code
          }`,
          gross: "-",
        },
      ]
    },

    fieldsPrices() {
      return [
        {
          key: "net",
          sortable: false,
        },
        {
          key: "vat",
          sortable: false,
        },
        {
          key: "gross",
          sortable: false,
        },
      ]
    },

    // https://stackoverflow.com/questions/8073673/how-can-i-add-new-array-elements-at-the-beginning-of-an-array-in-javascript

    fieldsItemPrices() {
      return [{ key: "x", label: "Item", sortable: false }].concat(
        this.fieldsPrices
      )
    },
    fieldsShipmentPrices() {
      return [{ key: "x", label: "Shipment", sortable: false }].concat(
        this.fieldsPrices
      )
    },
    fieldsGiftWrapPrices() {
      return [{ key: "x", label: "Gift Wrap", sortable: false }].concat(
        this.fieldsPrices
      )
    },
    fieldsTotalPrices() {
      return [{ key: "x", label: "Total", sortable: false }].concat(
        this.fieldsPrices
      )
    },
  },
}
</script>

<style>
</style>
