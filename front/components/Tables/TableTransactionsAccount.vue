<template>
    <div>
        Boom Boom {{ channelCode }}<br><br>

        <b-table :fields="fields" :items="transactions" hover>

            <template v-slot:cell(identifier)="data">
                Marketplace: {{ data.value.marketplace}} <br>
                Public Transaction Type: {{ data.value.transaction_type_public_code }} <br>
                Public ID: {{ data.value.given_id }} <br>
                Activity ID: {{ data.value.activity_id }}
                Link: <nuxt-link :to="data.item.public_id" append >{{ data.value }}</nuxt-link>
            </template>

            <template v-slot:cell(dates)="data">
                Shipment Date: {{ data.value.shipment_date}} <br>
                Arrival Date: {{ data.value.arrival_date }} <br>
                Complete Date: {{ data.value.complete_date }}
            </template>

            <template v-slot:cell(item)="data">
                Name: {{ data.value.item_name }} <i>(SKU: {{ data.value.item_sku }})</i><br>
                Quantity: {{ data.value.item_quantity }} <br>
                Weight: {{ data.value.item_weight_kg }}kg <br>
                Weight Total: {{ data.value.item_weight_kg_total }}kg
            </template>

            <template v-slot:cell(itemPrices)="data">
                Discount Gross: {{ data.value.item_price_discount_gross }}{{ data.value.currency_code }}<br>
                Gross: {{ data.value.item_price_gross }}{{ data.value.currency_code }} <br>
                Total Gross: {{ data.value.item_price_total_gross }}{{ data.value.currency_code }}
            </template>

            <template v-slot:cell(shipmentPrices)="data">
                Discount Gross: {{ data.value.shipment_price_discount_gross }}{{ data.value.currency_code }}<br>
                Gross: {{ data.value.shipment_price_gross }}{{ data.value.currency_code }} <br>
                Total Gross: {{ data.value.shipment_price_total_gross }}{{ data.value.currency_code }}
            </template>

            <template v-slot:cell(giftWrapPrices)="data">
                Discount Gross: {{ data.value.gift_wrap_price_discount_gross }}{{ data.value.currency_code }}<br>
                Gross: {{ data.value.gift_wrap_price_gross }}{{ data.value.currency_code }} <br>
                Total Gross: {{ data.value.gift_wrap_price_total_gross }}{{ data.value.currency_code }}
            </template>

            <template v-slot:cell(departureAddress)="data">
                {{ data.value.departure_postal_code }} {{ data.value.departure_city }} <br>
                {{ data.value.departure_country_code }}
            </template>

            <template v-slot:cell(arrivalAddress)="data">
                {{ data.value.arrival_postal_code }} {{ data.value.arrival_city }} <br>
                {{ data.value.arrival_country_code }}
            </template>

            <template v-slot:cell(shipment)="data">
                Mode: {{ data.value.shipment_mode }}<br>
                Conditions: {{ data.value.shipment_conditions }}
            </template>

            <template v-slot:cell(invoice)="data">
                {{ data.value.invoice_number }}<br>
                TODO: external link to --> {{ data.value.invoice_url}}
            </template>

            <template v-slot:cell(customer)="data">
                Vat Number: {{ data.value.customer_firm_vat_number }}<br>
            </template>

            <template v-slot:cell(supplier)="data">
                Vat Number: {{ data.value.supplier_vat_number }}<br>
                Name: {{ data.value.supplier_name }}
            </template>

        </b-table>
    </div>
</template>

<script>
export default {
    name: 'TableTransactionsAccount',

    props: {
        // eslint-disable-next-line
        channelCode: {
            type: [Array],
            required: false

        }

    },

    data() {
        return {
            fields: [
                {
                    key: 'publicActivityPeriod',
                    sortable: true,
                },
                {
                    key: 'identifier',
                    sortable: true,
                },
                {
                    key: 'dates',
                    sortable: true,
                },
                {
                    key: 'item',
                    sortable: true,
                },
                {
                    key: 'itemPrices',
                    sortable: true,
                },
                {
                    key: 'shipmentPrices',
                    sortable: true,
                },
                {
                    key: 'giftWrapPrices',
                    sortable: true,
                },
                {
                    key: 'saleTotalValueGross',
                    sortable: true,
                },
                {
                    key: 'departureAddress',
                    sortable: false,
                },
                {
                    key: 'arrivalAddress',
                    sortable: false,
                },
                {
                    key: 'shipment',
                    sortable: false,
                },
                {
                    key: 'invoice',
                    sortable: false,
                },
                {
                    key: 'customer',
                    sortable: false,
                },
                {
                    key: 'supplier',
                    sortable: false,
                }
            ]
        }
    },

    computed: {
        transactions() {
            return this.$store.getters["seller_firm/accountTransactionInputs"](this.channelCode);
        }
    }
}
</script>

<style>

</style>
