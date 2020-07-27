<template>
    <div>
        <b-card-group deck class="my-5">
            <b-card
                title="Base Data"
            >
                <b-row cols="2">
                    <b-col>
                        <b>Tax Jurisdiction:</b> {{ transaction.tax_jurisdiction }} <br>
                        <b>Departure Country</b> {{ transaction.departure_country }}<br>
                        <b>Arrival Country:</b> {{ transaction.arrival_country }} <br><br>
                    </b-col>
                    <b-col>
                        <b>Type:</b> {{ transaction.type_code }}<br>
                        <b>Tax Treatment:</b> {{ transaction.tax_treatment_code }} <br>
                        <b>Item:</b> Tax Code: {{ transaction.item_tax_code_code }} | Tax Rate Type: {{ transaction.item_tax_rate_type_code }}<br>
                        <b>Shipment:</b> Tax Rate Type: {{ transaction.shipment_tax_rate_type_code }}<br>
                        <b>Gift Wrap:</b> Tax Rate Type: {{ transaction.gift_wrap_tax_rate_type_code }}<br>
                    </b-col>
                </b-row>
            </b-card>

            <b-card
                title="Values"
            >
                <b-row cols="2">
                    <b-col>
                        <b>Total Values</b>
                        <p>Net: {{ transaction.total_value_net }} {{ transaction.transaction_currency }}</p>
                        <p>Vat: {{ transaction.total_value_vat }} {{ transaction.transaction_currency }}</p>
                        <p>Gross: {{ transaction.total_value_gross }} {{ transaction.transaction_currency }}</p>
                    </b-col>

                    <b-col>
                        <b>Invoice</b>
                        <p>Exchange Rate: {{ transaction.invoice_exchange_rate }}  <i>({{ transaction.invoice_exchange_rate_date }})</i></p>
                        <p>Net: {{ transaction.invoice_amount_net }} {{ transaction.transaction_currency }}</p>
                        <p>Vat: {{ transaction.invoice_amount_vat }} {{ transaction.transaction_currency }}</p>
                        <p>Gross: {{ transaction.invoice_amount_gross }} {{ transaction.invoice_currency }}</p>
                        <p>Amount Reverse Charge: {{ transaction.invoice_amount_vat_reverse_charge}} {{ transaction.invoice_currency }}</p>
                    </b-col>
                </b-row>
            </b-card>
        </b-card-group>
        <b-card-group>
            <b-card
                title="Dates"
            >
                <b>Tax Date:</b> {{ transaction.tax_date }} <br>
                <b>Tax Calculation Date:</b> {{ transaction.tax_calculation_date }} <br>
            </b-card>
            <b-card
                title="Customer"
            >
                <b>Name:</b> {{ transaction.customer_firm_name }} <br>
                <b>Relationship:</b> {{ transaction.customer_relationship }} | VATIN: {{ transaction.customer_firm_vatin }} | Verified:  {{ transaction.customer_relationship_checked }}
            </b-card>
        </b-card-group>
        <b-card-group>
            <b-card title="Prices">
                <b-table striped hover borderless :items="items" :fields="fields"></b-table>
            </b-card>

        </b-card-group>
    </div>
</template>

<script>
    export default {
        name: 'CardTransaction',
        props: {
            transaction: {
                type: [Array, Object],
                required: true
            }
        },
        computed: {
            items() {
                return [
                    {
                        x: 'Item',
                        price_vat_rate: this.transaction.item_price_vat_rate,
                        price_net: this.transaction.item_price_net,
                        price_discount_net: this.transaction.item_price_discount_net,
                        price_total: this.transaction.item_price_total_net,
                        price_vat: this.transaction.item_price_vat,
                        price_discount_vat: this.transaction.item_price_discount_vat,
                        price_total_vat: this.transaction.item_price_total_vat
                    },
                    {
                        x: 'Shipment',
                        price_vat_rate: this.transaction.shipment_price_vat_rate,
                        price_net: this.transaction.shipment_price_net,
                        price_discount_net: this.transaction.shipment_price_discount_net,
                        price_total_net: this.transaction.shipment_price_total_net,
                        price_vat: this.transaction.shipment_price_vat,
                        price_discount_vat: this.transaction.shipment_price_discount_vat,
                        price_total_vat: this.transaction.shipment_price_total_vat
                    },
                    {
                        x: 'Gift Wrap',
                        price_vat_rate: this.transaction.gift_wrap_price_vat_rate,
                        price_net: this.transaction.gift_wrap_price_net,
                        price_discount_net: this.transaction.gift_wrap_price_discount_net,
                        price_total_net: this.transaction.gift_wrap_price_total_net,
                        price_vat: this.transaction.gift_wrap_price_vat,
                        price_discount_vat: this.transaction.gift_wrap_price_discount_vat,
                        price_total_vat: this.transaction.gift_wrap_price_total_vat
                    }
                ]


            },

            fields() {
                return [
                    {
                        key: 'x',
                        label:'',
                        sortable: false,
                    },
                    {
                        key: 'price_vat_rate',
                        label: 'Vat Rate',
                        sortable: false,
                    },
                    {
                        key: 'price_net',
                        label: `Price Net (in ${ this.transaction.transaction_currency})`,
                        sortable: false,
                    },
                    {
                        key: 'price_discount_net',
                        label: `Price Discount Net (in ${ this.transaction.transaction_currency})`,
                        sortable: false,
                    },
                    {
                        key: 'price_total_net',
                        label: `Price Total Vat (in ${ this.transaction.transaction_currency})`,
                        sortable: false,
                    },
                    {
                        key: 'price_vat',
                        label: `Price Vat (in ${ this.transaction.transaction_currency})`,
                        sortable: false,
                    },
                    {
                        key: 'price_discount_vat',
                        label: `Price Discount Vat (in ${ this.transaction.transaction_currency})`,
                        sortable: false,
                    },
                    {
                        key: 'price_total_vat',
                        label: `Price Total Vat (in ${ this.transaction.transaction_currency})`,
                        sortable: false,
                    }
                ]
            }
        },
    };
</script>

<style>
</style>
