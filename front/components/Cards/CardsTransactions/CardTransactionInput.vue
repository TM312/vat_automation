<template>
    <div>
        <b-card-group deck class="my-5">
            <b-card
                title="Base Data"
            >
                <b-row cols="2">
                    <b-col>
                        <b>Activity ID:</b> {{ transactionInput.activity_id }} <br>
                        <b>Public Activity Period</b> {{ transactionInput.public_activity_period }}<br>
                        <b>Original Filename:</b> {{ transactionInput.original_filename }}
                    </b-col>
                    <b-col>
                        <b>Account:</b> {{ transactionInput.account_given_id }}<br>
                        <b>Channel:</b> {{ transactionInput.channel_code }} <br>
                        <b>Marketplace</b> {{ transactionInput.marketplace }}<br>
                        <b>Public Transaction Type:</b> {{ transactionInput.transaction_type_public_code }}
                    </b-col>
                </b-row>

                <b>Created On:</b> {{ transactionInput.created_on }} <br>
                <b>Uploaded By:</b> {{ transactionInput.created_by }} <br>
            </b-card>
            <b-card
                title="Item"
            >
                <b>SKU:</b> {{ transactionInput.item_sku }} <br>
                <b>Name</b> {{ transactionInput.item_name }} <br>
                <b>Quantity:</b> {{ transactionInput.item_quantity }}<br>
                <b>Manufacture Country:</b> {{ transactionInput.item_manufacture_country }} <br>
                <b>Weight:</b> {{ transactionInput.item_weight_kg }}kg <i>(Total:{{ transactionInput.item_weight_kg_total }}kg</i>
            </b-card>

        </b-card-group>
        <b-card-group deck>
            <b-card title="Logistics">
                <b-row cols="3">
                    <b-col>
                        <b>Departure</b><br>
                        {{ transactionInput.departure_country_code }}<br>
                        {{ transactionInput.departure_postal_code }} {{ transactionInput.departure_city }}<br>
                        <br>
                        <b>Arrival</b><br>
                        {{ transactionInput.arrival_country_code }}<br>
                        {{ transactionInput.arrival_postal_code }} {{ transactionInput.arrival_city }}<br>
                        {{ transactionInput.arrival_address }}
                    </b-col>
                    <b-col>
                        <b>Shipment</b><br>
                        <b>Mode:</b> {{ transactionInput.shipment_mode }} <br>
                        <b>Conditions:</b> {{ transactionInput.shipment_conditions }} <br>
                    </b-col>
                    <b-col>
                        <b>Dates</b><br>
                        <b>Shipment:</b> {{ transactionInput.shipment_date }} <br>
                        <b>Arrival:</b> {{ transactionInput.arrival_date }} <br>
                        <b>Complete:</b> {{ transactionInput.complete_date }} <br>




                    </b-col>
                </b-row>
            </b-card>
            <b-card title="Prices">
                <b-table striped hover borderless :items="items" :fields="fields"></b-table>

            </b-card>
        </b-card-group>
    </div>

</template>

<script>
import { mapState } from 'vuex'
export default {
    name:'CardTransactionInput',

    computed: {
        ...mapState({
            transactionInput: state => state.transaction_input.transaction_input
        }),

        // alertStatus() {
        //     return this.transactionInput.processed ? 'success' : 'warning'
        // },
        items() {
            return [
                {
                    x: 'Item',
                    price_gross: this.transactionInput.item_price_gross,
                    price_discount: this.transactionInput.item_price_discount_gross,
                    price_total: this.transactionInput.item_price_total_gross
                },
                {
                    x: 'Shipment',
                    price_gross: this.transactionInput.shipment_price_gross,
                    price_discount: this.transactionInput.shipment_price_discount_gross,
                    price_total: this.transactionInput.shipment_price_total_gross
                },
                {
                    x: 'Gift Wrap',
                    price_gross: this.transactionInput.gift_wrap_price_gross,
                    price_discount: this.transactionInput.gift_wrap_price_discount_gross,
                    price_total: this.transactionInput.gift_wrap_price_total_gross
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
                    key: 'price_gross',
                    label: `Price Gross (in ${ this.transactionInput.currency_code})`,
                    sortable: false,
                },
                {
                    key: 'price_discount',
                    label: `Price Discount (in ${ this.transactionInput.currency_code})`,
                    sortable: false,
                },
                {
                    key: 'price_total',
                    label: `Price Total (in ${ this.transactionInput.currency_code})`,
                    sortable: false,
                }
            ]
        }
    }

}
</script>
